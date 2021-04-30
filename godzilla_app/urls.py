from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('monster_island', views.monster_island),
    path('detail/<int:movie_id>', views.movie_detail),
    path('collection/<int:collection_id>', views.collection),
    path('collection/all', views.all_films),
    path('messages/<int:movie_id>', views.message_post),
    path('comments/<int:message_id>', views.comment_post),
    path('watchlist', views.watchlist)
]