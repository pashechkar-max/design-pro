from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('profile/', views.profile , name='profile'),
    path('register/', views.register , name='register'),
    path('create/', views.create_design_request, name='create'),
]