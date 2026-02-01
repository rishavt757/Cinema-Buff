from django.contrib import admin
from .models import Genre, Movie, Rating, Review, Watchlist, Favorite, RatingStats

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'average_rating', 'total_ratings', 'created_at']
    list_filter = ['genres', 'release_date', 'created_at']
    search_fields = ['title', 'synopsis']
    filter_horizontal = ['genres']
    readonly_fields = ['average_rating', 'total_ratings']
    ordering = ['-created_at']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'overall_score', 'story_score', 'acting_score', 'cinematography_score', 'created_at']
    list_filter = ['overall_score', 'created_at', 'user__profile__role']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-created_at']
    readonly_fields = ['is_critic_rating', 'weighted_score']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'movie__title', 'title', 'content']
    ordering = ['-created_at']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-added_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-added_at']

@admin.register(RatingStats)
class RatingStatsAdmin(admin.ModelAdmin):
    list_display = ['movie', 'total_ratings', 'user_ratings_count', 'critic_ratings_count', 'weighted_average', 'updated_at']
    list_filter = ['total_ratings', 'updated_at']
    search_fields = ['movie__title']
    readonly_fields = ['movie', 'total_ratings', 'user_ratings_count', 'critic_ratings_count', 
                      'weighted_average', 'user_average', 'critic_average', 
                      'story_average', 'acting_average', 'cinematography_average']
    ordering = ['-updated_at']
