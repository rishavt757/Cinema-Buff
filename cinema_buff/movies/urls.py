from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('create/', views.MovieCreateView.as_view(), name='movie_create'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:pk>/rate/', views.RateMovieView.as_view(), name='rate_movie'),
    path('<int:pk>/review/', views.ReviewMovieView.as_view(), name='review_movie'),
    path('my-ratings/', views.MyRatingsView.as_view(), name='my_ratings'),
    path('watchlist/', views.WatchlistView.as_view(), name='watchlist'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('add-to-watchlist/<int:movie_id>/', views.AddToWatchlistView.as_view(), name='add_to_watchlist'),
    path('remove-from-watchlist/<int:movie_id>/', views.RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
    path('add-to-favorites/<int:movie_id>/', views.AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('remove-from-favorites/<int:movie_id>/', views.RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
]
