from django.urls import path
from .views import *

app_name='subsite'

urlpatterns=[
    path('',index),
    path('blog/',blog),
]