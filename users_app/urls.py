from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('account/', views.account, name='account'),
    path('post_group/', views.post_group, name='post_group'),
    path('groups/', views.read_groups, name='groups'),
    path('groups/<int:group_pk>', views.read_group, name='read_group'),
    path('groups/<int:group_pk>/update_group', views.update_group, name='update_group'),
    path('groups/<int:group_pk>/delete_group', views.delete_group, name='delete_group'),
]
