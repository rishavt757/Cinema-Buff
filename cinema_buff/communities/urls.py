from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.CommunityListView.as_view(), name='community_list'),
    path('<int:pk>/', views.CommunityDetailView.as_view(), name='community_detail'),
    path('join/<int:community_id>/', views.JoinCommunityView.as_view(), name='join_community'),
    path('leave/<int:community_id>/', views.LeaveCommunityView.as_view(), name='leave_community'),
    path('<int:community_id>/create/', views.CreateDiscussionPostView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.DiscussionPostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/comment/', views.AddCommentView.as_view(), name='add_comment'),
]
