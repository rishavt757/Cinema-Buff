from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    release_date = models.DateField()
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CONTENT_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
    ]
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='movie')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Calculate weighted average rating using calculated overall scores"""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        
        total_weighted_score = sum(rating.weighted_score for rating in ratings)
        total_weight = sum(2.0 if rating.is_critic_rating else 1.0 for rating in ratings)
        
        return round(total_weighted_score / total_weight, 1)
    
    @property
    def user_average_rating(self):
        """Calculate average rating for regular users only using calculated scores"""
        user_ratings = self.ratings.filter(user__profile__role='user')
        if not user_ratings:
            return 0
        return round(sum(r.calculated_overall_score for r in user_ratings) / len(user_ratings), 1)
    
    @property
    def critic_average_rating(self):
        """Calculate average rating for critics only using calculated scores"""
        critic_ratings = self.ratings.filter(user__profile__role='critic')
        if not critic_ratings:
            return 0
        return round(sum(r.calculated_overall_score for r in critic_ratings) / len(critic_ratings), 1)
    
    @property
    def average_story_rating(self):
        """Calculate average story rating"""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(rating.story_score for rating in ratings) / len(ratings), 1)
    
    @property
    def average_acting_rating(self):
        """Calculate average acting rating"""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(rating.acting_score for rating in ratings) / len(ratings), 1)
    
    @property
    def average_cinematography_rating(self):
        """Calculate average cinematography rating"""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(rating.cinematography_score for rating in ratings) / len(ratings), 1)

    @property
    def total_ratings(self):
        return self.ratings.count()

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    
    # Overall rating (1-10 for more granularity)
    overall_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    
    # Legacy field for migration
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Legacy 1-5 rating (will be migrated to 1-10 scale)"
    )
    
    # Detailed ratings (1-10)
    story_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating for story/plot (1-10)",
        default=5
    )
    acting_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating for acting performance (1-10)",
        default=5
    )
    cinematography_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating for cinematography (1-10)",
        default=5
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        score_display = self.overall_score or self.score
        return f"{self.user.username} - {self.movie.title} - {score_display}"
    
    @property
    def effective_score(self):
        """Get the effective rating score (calculated as average of detailed scores)"""
        if self.overall_score:
            # For legacy ratings, use the manual overall score
            return self.overall_score
        elif self.score:
            # Convert 1-5 scale to 1-10 scale
            return self.score * 2
        else:
            # Calculate average of detailed scores
            return round((self.story_score + self.acting_score + self.cinematography_score) / 3, 1)
    
    @property
    def calculated_overall_score(self):
        """Calculate overall score as average of detailed scores"""
        return round((self.story_score + self.acting_score + self.cinematography_score) / 3, 1)
    
    @property
    def is_critic_rating(self):
        """Check if this is a critic rating"""
        return self.user.profile.role == 'critic'
    
    @property
    def weighted_score(self):
        """Calculate weighted score based on user role"""
        base_weight = 2.0 if self.is_critic_rating else 1.0
        return self.calculated_overall_score * base_weight

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='in_watchlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class RatingStats(models.Model):
    """Pre-calculated rating statistics for better performance"""
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='rating_stats')
    
    # Overall statistics
    total_ratings = models.IntegerField(default=0)
    user_ratings_count = models.IntegerField(default=0)
    critic_ratings_count = models.IntegerField(default=0)
    
    # Average ratings
    weighted_average = models.FloatField(default=0.0)
    user_average = models.FloatField(default=0.0)
    critic_average = models.FloatField(default=0.0)
    
    # Category averages
    story_average = models.FloatField(default=0.0)
    acting_average = models.FloatField(default=0.0)
    cinematography_average = models.FloatField(default=0.0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.movie.title} - Stats"
    
    @classmethod
    def update_stats(cls, movie):
        """Update rating statistics for a movie using calculated scores"""
        ratings = movie.ratings.all()
        
        if not ratings.exists():
            # Delete stats if no ratings exist
            cls.objects.filter(movie=movie).delete()
            return
        
        stats, created = cls.objects.get_or_create(movie=movie)
        
        # Update counts
        stats.total_ratings = ratings.count()
        stats.user_ratings_count = ratings.filter(user__profile__role='user').count()
        stats.critic_ratings_count = ratings.filter(user__profile__role='critic').count()
        
        # Update averages using calculated scores
        stats.weighted_average = movie.average_rating
        stats.user_average = movie.user_average_rating
        stats.critic_average = movie.critic_average_rating
        stats.story_average = movie.average_story_rating
        stats.acting_average = movie.average_acting_rating
        stats.cinematography_average = movie.average_cinematography_rating
        
        stats.save()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='in_favorites')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
