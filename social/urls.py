from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and Posts
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='social/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ✅ Will redirect to /login/
    path('signup/', views.signup, name='signup'),

    # Search
    path('search/', views.search_users, name='search_users'),

    # Profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
