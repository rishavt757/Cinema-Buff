from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Community, CommunityMember, DiscussionPost, DiscussionComment
from movies.models import Movie
from .forms import DiscussionPostForm, DiscussionCommentForm

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
        context['posts'] = community.posts.all().select_related('author').prefetch_related('comments')
        
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

class CreateDiscussionPostView(LoginRequiredMixin, CreateView):
    model = DiscussionPost
    form_class = DiscussionPostForm
    template_name = 'communities/create_post.html'

    def form_valid(self, form):
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        
        # Check if user is a member
        if not CommunityMember.objects.filter(community=community, user=self.request.user).exists():
            messages.error(self.request, 'You must join the community before posting.')
            return redirect('communities:community_detail', pk=community.pk)
        
        form.instance.author = self.request.user
        form.instance.community = community
        response = super().form_valid(form)
        
        messages.success(self.request, 'Your discussion post has been created!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('communities:community_detail', kwargs={'pk': self.kwargs['community_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = get_object_or_404(Community, pk=self.kwargs['community_id'])
        return context

class DiscussionPostDetailView(DetailView):
    model = DiscussionPost
    template_name = 'communities/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        context['comments'] = post.comments.all().select_related('author')
        context['comment_form'] = DiscussionCommentForm()
        
        if self.request.user.is_authenticated:
            context['is_member'] = CommunityMember.objects.filter(
                community=post.community,
                user=self.request.user
            ).exists()
        
        return context

class AddCommentView(LoginRequiredMixin, CreateView):
    model = DiscussionComment
    form_class = DiscussionCommentForm

    def form_valid(self, form):
        post = get_object_or_404(DiscussionPost, pk=self.kwargs['post_id'])
        
        # Check if user is a member
        if not CommunityMember.objects.filter(community=post.community, user=self.request.user).exists():
            messages.error(self.request, 'You must join the community before commenting.')
            return redirect('communities:post_detail', pk=post.pk)
        
        form.instance.author = self.request.user
        form.instance.post = post
        response = super().form_valid(form)
        
        messages.success(self.request, 'Your comment has been added!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('communities:post_detail', kwargs={'pk': self.kwargs['post_id']})
