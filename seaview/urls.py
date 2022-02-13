from django.urls import path, include
from . import views


app_name = 'seaview'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:review_id>/', views.detail, name = 'detail'),
    path('reply/create/<int:review_id>/', views.reply_create, name='reply_create'),
    path('search/', include('movieapi.urls')),
    path('review/create/', views.review_create, name='review_create'),
    path('seaview/modify/<int:review_id>/', views.review_modify, name='review_modify'),
    path('review/delete/<int:review_id>/', views.review_delete, name='review_delete'),
    path('seaview/modify/<int:reply_id>/', views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:answer_id>/', views.reply_delete, name = 'reply_delete'),
    path('vote/review/<int:review_id>/', views.vote_review, name='vote_review'),
]