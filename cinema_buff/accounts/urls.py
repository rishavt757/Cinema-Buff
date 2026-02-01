from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('connect/<int:user_id>/', views.ConnectView.as_view(), name='connect'),
    path('disconnect/<int:user_id>/', views.DisconnectView.as_view(), name='disconnect'),
    path('connections/', views.ConnectionsView.as_view(), name='connections'),
]
