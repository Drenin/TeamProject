from django.urls import path, include
from . import views


app_name = 'seaview'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:review_id>/', views.detail, name = 'detail'),
    #path('reply/create/<int:review_id>/', views.reply_create, name='reply_create'),
    path('search/', include('movieapi.urls')),
]