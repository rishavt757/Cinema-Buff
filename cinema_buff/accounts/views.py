from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, RedirectView, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, UserConnection
from .forms import UserProfileForm

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure fresh data from database
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been updated successfully!")
        return response

class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['user_profile'] = profile_user.profile
        if self.request.user.is_authenticated:
            context['is_connected'] = UserConnection.objects.filter(
                from_user=self.request.user,
                to_user=profile_user
            ).exists()
        return context

class ConnectView(LoginRequiredMixin, DetailView):
    model = User
    pk_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        to_user = self.get_object()
        if to_user != request.user:
            UserConnection.objects.get_or_create(
                from_user=request.user,
                to_user=to_user
            )
            messages.success(request, f"You are now connected with {to_user.username}")
        return redirect('accounts:user_profile', user_id=to_user.id)

class DisconnectView(LoginRequiredMixin, DetailView):
    model = User
    pk_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        to_user = self.get_object()
        UserConnection.objects.filter(
            from_user=request.user,
            to_user=to_user
        ).delete()
        messages.success(request, f"You are no longer connected with {to_user.username}")
        return redirect('accounts:user_profile', user_id=to_user.id)

class ConnectionsView(LoginRequiredMixin, ListView):
    model = UserConnection
    template_name = 'accounts/connections.html'
    context_object_name = 'connections'

    def get_queryset(self):
        return UserConnection.objects.filter(from_user=self.request.user).select_related('to_user')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        
        # Get the previous page URL
        next_page = request.META.get('HTTP_REFERER')
        if next_page and 'logout' not in next_page:
            return redirect(next_page)
        else:
            return redirect('home')
