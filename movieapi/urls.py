from django.urls import path, re_path
from movieapi import views
from movieapi.views import index

app_name='movieapi'

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^search/', views.search, name='api_search')
]