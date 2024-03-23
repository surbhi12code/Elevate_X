from django.urls import path
from .import views

urlpatterns = [
    path('', views.home,name='home'),
    path('getHired',views.getHired,name='getHired'),
    path('doquiz',views.doquiz, name='doquiz'),
    path('job-listing/',views.job_listing,name='job-listing'),
    path('job-details/<int:pk>/', views.job_details, name='job-details')

]