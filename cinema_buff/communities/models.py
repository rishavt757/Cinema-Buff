from django.db import models
from django.contrib.auth.models import User
from movies.models import Genre

class Community(models.Model):
    genre = models.OneToOneField(Genre, on_delete=models.CASCADE, related_name='community')
    name = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='community_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()
    
    @property
    def post_count(self):
        return self.posts.count()

class CommunityMember(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('community', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.community.name}"

class DiscussionPost(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.community.name}"

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def recent_activity(self):
        latest_comment = self.comments.order_by('-created_at').first()
        return latest_comment.created_at if latest_comment else self.created_at

class DiscussionComment(models.Model):
    post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
