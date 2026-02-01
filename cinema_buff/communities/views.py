from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Community, CommunityMember
from movies.models import Movie

class CommunityListView(ListView):
    model = Community
    template_name = 'communities/community_list.html'
    context_object_name = 'communities'

    def get_queryset(self):
        return Community.objects.all().select_related('genre').prefetch_related('members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_communities = CommunityMember.objects.filter(user=self.request.user).values_list('community_id', flat=True)
            context['user_communities'] = set(user_communities)
        return context

class CommunityDetailView(DetailView):
    model = Community
    template_name = 'communities/community_detail.html'
    context_object_name = 'community'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = self.get_object()
        
        context['movies'] = Movie.objects.filter(genres=community.genre).prefetch_related('genres', 'ratings')
        context['members'] = CommunityMember.objects.filter(community=community).select_related('user')
        
        if self.request.user.is_authenticated:
            context['is_member'] = CommunityMember.objects.filter(
                community=community,
                user=self.request.user
            ).exists()
        
        return context

class JoinCommunityView(LoginRequiredMixin, DetailView):
    model = Community
    pk_url_kwarg = 'community_id'

    def get(self, request, *args, **kwargs):
        community = self.get_object()
        member, created = CommunityMember.objects.get_or_create(
            community=community,
            user=request.user
        )
        
        if created:
            messages.success(request, f'You have joined the {community.name} community!')
        else:
            messages.info(request, f'You are already a member of the {community.name} community!')
        
        return redirect('communities:community_detail', pk=community.pk)

class LeaveCommunityView(LoginRequiredMixin, DetailView):
    model = Community
    pk_url_kwarg = 'community_id'

    def get(self, request, *args, **kwargs):
        community = self.get_object()
        CommunityMember.objects.filter(
            community=community,
            user=request.user
        ).delete()
        
        messages.success(request, f'You have left the {community.name} community!')
        return redirect('communities:community_detail', pk=community.pk)
