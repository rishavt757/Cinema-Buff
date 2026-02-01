from django.contrib import admin
from .models import Genre, Movie, Rating, Review, Watchlist, Favorite

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
    list_display = ['user', 'movie', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-created_at']

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
