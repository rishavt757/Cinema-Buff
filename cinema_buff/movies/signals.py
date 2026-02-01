from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating, RatingStats

@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def update_rating_stats(sender, instance, **kwargs):
    """Update rating statistics when a rating is saved or deleted"""
    RatingStats.update_stats(instance.movie)
