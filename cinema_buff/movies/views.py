from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Avg, Q
from .models import Movie, Genre, Rating, Review, Watchlist, Favorite
from .forms import RatingForm, ReviewForm, MovieCreateForm

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        queryset = Movie.objects.all().prefetch_related('genres', 'ratings')
        
        # Handle search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(synopsis__icontains=search_query)
            ).distinct()
        
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'highest_rated':
            queryset = queryset.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
        elif sort_by == 'lowest_rated':
            queryset = queryset.annotate(avg_rating=Avg('ratings__score')).order_by('avg_rating')
        elif sort_by == 'my_ratings':
            if self.request.user.is_authenticated:
                user_rated_movies = Rating.objects.filter(user=self.request.user).values_list('movie_id', flat=True)
                queryset = queryset.filter(id__in=user_rated_movies)
            else:
                queryset = queryset.none()
        
        genre_filter = self.request.GET.get('genre')
        if genre_filter:
            queryset = queryset.filter(genres__name=genre_filter)
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['current_genre'] = self.request.GET.get('genre', '')
        context['current_search'] = self.request.GET.get('search', '')
        
        # Check if user can add movies (critic or admin)
        if self.request.user.is_authenticated:
            user_role = getattr(self.request.user.profile, 'role', 'user')
            context['can_add_movie'] = user_role in ['critic', 'admin']
        else:
            context['can_add_movie'] = False
            
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        
        if self.request.user.is_authenticated:
            context['user_rating'] = Rating.objects.filter(user=self.request.user, movie=movie).first()
            context['user_review'] = Review.objects.filter(user=self.request.user, movie=movie).first()
            context['in_watchlist'] = Watchlist.objects.filter(user=self.request.user, movie=movie).exists()
            context['is_favorite'] = Favorite.objects.filter(user=self.request.user, movie=movie).exists()
        
        context['reviews'] = movie.reviews.all().order_by('-created_at')
        return context

class RateMovieView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'movies/rate_movie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['movie'] = movie
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        form.instance.movie = movie
        
        rating, created = Rating.objects.update_or_create(
            user=self.request.user,
            movie=movie,
            defaults={'score': form.cleaned_data['score']}
        )
        
        messages.success(self.request, f'You rated "{movie.title}" {rating.score} stars!')
        return redirect('movies:movie_detail', pk=movie.pk)

class ReviewMovieView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'movies/review_movie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['movie'] = movie
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        form.instance.movie = movie
        
        review, created = Review.objects.update_or_create(
            user=self.request.user,
            movie=movie,
            defaults={
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content']
            }
        )
        
        messages.success(self.request, f'Your review for "{movie.title}" has been saved!')
        return redirect('movies:movie_detail', pk=movie.pk)

class MyRatingsView(LoginRequiredMixin, ListView):
    model = Rating
    template_name = 'movies/my_ratings.html'
    context_object_name = 'ratings'
    paginate_by = 12

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).select_related('movie').order_by('-updated_at')

class WatchlistView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = 'movies/watchlist.html'
    context_object_name = 'watchlist_items'
    paginate_by = 12

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user).select_related('movie').order_by('-added_at')

class FavoritesView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'movies/favorites.html'
    context_object_name = 'favorite_items'
    paginate_by = 12

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('movie').order_by('-added_at')

class AddToWatchlistView(LoginRequiredMixin, DetailView):
    model = Movie
    pk_url_kwarg = 'movie_id'

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        Watchlist.objects.get_or_create(user=request.user, movie=movie)
        messages.success(request, f'"{movie.title}" added to your watchlist!')
        return redirect('movies:movie_detail', pk=movie.pk)

class RemoveFromWatchlistView(LoginRequiredMixin, DetailView):
    model = Movie
    pk_url_kwarg = 'movie_id'

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        Watchlist.objects.filter(user=request.user, movie=movie).delete()
        messages.success(request, f'"{movie.title}" removed from your watchlist!')
        return redirect('movies:movie_detail', pk=movie.pk)

class AddToFavoritesView(LoginRequiredMixin, DetailView):
    model = Movie
    pk_url_kwarg = 'movie_id'

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        Favorite.objects.get_or_create(user=request.user, movie=movie)
        messages.success(request, f'"{movie.title}" added to your favorites!')
        return redirect('movies:movie_detail', pk=movie.pk)

class RemoveFromFavoritesView(LoginRequiredMixin, DetailView):
    model = Movie
    pk_url_kwarg = 'movie_id'

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        Favorite.objects.filter(user=request.user, movie=movie).delete()
        messages.success(request, f'"{movie.title}" removed from your favorites!')
        return redirect('movies:movie_detail', pk=movie.pk)

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieCreateForm
    template_name = 'movies/movie_create.html'
    success_url = reverse_lazy('movies:movie_list')

    def dispatch(self, request, *args, **kwargs):
        # Check if user has permission to add movies
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        user_role = getattr(request.user.profile, 'role', 'user')
        if user_role not in ['critic', 'admin']:
            messages.error(request, 'You do not have permission to add movies.')
            return redirect('movies:movie_list')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Movie "{form.instance.title}" added successfully!')
        return super().form_valid(form)
