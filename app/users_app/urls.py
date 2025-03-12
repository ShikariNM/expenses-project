from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from django.urls import path

from .views import (
    LoginUser,
    RegisterUser,
    Account,
    UserPasswordChangeView,
    UserPasswordResetView,
    UserPasswordResetConfirmView,
    post_group,
    read_groups,
    read_group,
    update_group,
    delete_group,
)

app_name = 'users'


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('account/', Account.as_view(), name='account'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="users_app/password_change_done.html"),
         name='password_change_done'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users_app/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users_app/password_reset_complete.html'),
         name='password_reset_complete'),

    path('post_group/', post_group, name='post_group'),
    path('groups/', read_groups, name='groups'),
    path('groups/<int:group_pk>', read_group, name='read_group'),
    path('groups/<int:group_pk>/update_group', update_group, name='update_group'),
    path('groups/<int:group_pk>/delete_group', delete_group, name='delete_group'),
]
