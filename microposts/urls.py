from django.urls import path
from .views import (
    PostCreateView, PostListView, 
    PostUpdateView, PostDeleteView,
    MyPostsView, 
    FollowersView, FollowingView,
    GalleryView,# 追加
)
from . import views 

app_name = 'microposts'
urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('postlist/', PostListView.as_view(), name='postlist'), 
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('myposts/', MyPostsView.as_view(), name='myposts'),
    path('add_favourite/<int:pk>/', views.add_favourite, name='add_favourite'),
    path('rm_favourite/<int:pk>/', views.remove_favourite, name='rm_favourite'),
    path('follower/', FollowersView.as_view(), name='follower'), 
    path('following/', FollowingView.as_view(), name='following'), 
    path('gallery/', GalleryView.as_view(), name='gallery'), # 追加
    path('add_file/', views.add_file, name='add_file'), # 追加    
]