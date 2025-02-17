from django.urls import path
from . import views

urlpatterns = [
    path('user-info/', views.user_info, name='user_info'),
    path('check-news/', views.check_news, name='check_news'),
]

