from django.urls import path
from .import views

urlpatterns = [
    path('register-applicant/', views.register_applicant,name="register-applicant"),
    path('register-recuriter/', views.register_recuriter,name='register-recuriter'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    
]