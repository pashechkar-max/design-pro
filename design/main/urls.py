from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('profile/', views.profile , name='profile'),
    path('register/', views.register , name='register'),
    path('create/', views.create_design_request, name='create'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('request/<int:request_id>/delete/', views.delete_design_request, name='delete_request'),
]