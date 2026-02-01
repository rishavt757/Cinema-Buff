from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from ..models import RatingStats

register = template.Library()

@register.filter
def rating_stars(value, max_stars=10):
    """Display rating as stars"""
    try:
        rating = float(value)
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = max_stars - full_stars - half_star
        
        stars_html = ""
        for _ in range(full_stars):
            stars_html += '<span class="star full">★</span>'
        if half_star:
            stars_html += '<span class="star half">★</span>'
        for _ in range(empty_stars):
            stars_html += '<span class="star empty">☆</span>'
        
        return mark_safe(f'<div class="rating-stars">{stars_html}</div>')
    except (ValueError, TypeError):
        return mark_safe('<div class="rating-stars"><span class="no-rating">Not Rated</span></div>')

@register.filter
def rating_percentage(value, max_value=10):
    """Convert rating to percentage for progress bars"""
    try:
        return (float(value) / max_value) * 100
    except (ValueError, TypeError):
        return 0

@register.simple_tag
def rating_breakdown(movie):
    """Get rating breakdown for a movie"""
    try:
        stats = movie.rating_stats
        if not stats:
            return None
        
        return {
            'overall': stats.weighted_average,
            'story': stats.story_average,
            'acting': stats.acting_average,
            'cinematography': stats.cinematography_average,
            'user_avg': stats.user_average,
            'critic_avg': stats.critic_average,
            'total_ratings': stats.total_ratings,
            'user_count': stats.user_ratings_count,
            'critic_count': stats.critic_ratings_count,
        }
    except RatingStats.DoesNotExist:
        return None

@register.filter
def role_badge(user_role):
    """Display user role as a badge"""
    badges = {
        'critic': '<span class="badge badge-critic">Critic</span>',
        'admin': '<span class="badge badge-admin">Admin</span>',
        'user': '<span class="badge badge-user">User</span>',
    }
    return mark_safe(badges.get(user_role, badges['user']))
