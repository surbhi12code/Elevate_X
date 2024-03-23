from django.urls import path
from . import views

urlpatterns = [
    path('',views.practice,name='practice'),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('about', views.about_view, name='about'),
    path('contact',views.about_view,name='contact'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('settings',views.editProfile,name='edit_profile'),
    path('delete',views.deleteProfile,name='delete_profile'),
    ]
