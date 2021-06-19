from django.urls import path
from .views import (
    RegistUserView,HomeView, 
    UserLoginView, UserLogoutView,
    ProfileEditView,UserListView, 
)
from . import views # 追加

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),  
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'), 
    path('userlist/', UserListView.as_view(), name='userlist'), 
    path('mk_relation/<int:pk>/', views.mk_relation, name='mk_relation'), # 追加
    path('rm_relation/<int:pk>/', views.rm_relation, name='rm_relation'), # 追加
]