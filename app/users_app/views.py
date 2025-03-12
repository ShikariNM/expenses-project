from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages

from .forms import (
    LoginUserForm,
    RegisterUserForm,
    PostGroupForm,
    AddUserToGroupForm,
    UpdateUserForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
)
from .models import CustomGroup


class LoginUser(LoginView):
    authentication_form = LoginUserForm
    template_name = 'users_app/login.html'
    extra_context = {'title': 'Authentication'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users_app/register.html'
    extra_context = {'title': "Registration"}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Your account has been registered successfully')
        return super().form_valid(form)


class Account(LoginRequiredMixin, UpdateView):
    form_class = UpdateUserForm
    template_name = 'users_app/account.html'
    context_object_name = 'user_being_changed'
    extra_context = {'title': 'My account'}
    success_url = reverse_lazy('users:account')

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been changed successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Try again')
        return super().form_invalid(form)


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users_app/password_change_form.html"


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users_app/password_reset_form.html'
    email_template_name = 'users_app/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'users_app/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")


@login_required
def read_groups(request):
    user = request.user
    return render(request, 'users_app/groups.html', {'title': 'Groups',
                                                     'content': user.groups.all()})


@login_required
def post_group(request):
    if request.method == 'POST':
        form = PostGroupForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not Group.objects.filter(name=cd['name']):
                new_group = Group(name=cd['name'])
                new_group.save()
                new_group.user_set.add(request.user)
                if request.user != cd['admin']:
                    new_group.user_set.add(cd['admin'])
                new_group.save()
                new_cust_group = CustomGroup(group=new_group,
                                             description=cd['description'],
                                             admin=cd['admin'])
                new_cust_group.save()
                messages.success(request, 'Group has been added')
            else:
                messages.error(request, 'A group with that name already exists')
        else:
            messages.error(request, 'Try again')
    else:
        form = PostGroupForm()
    return render(request, 'users_app/post_group.html', {'title': 'Post group',
                                                         'form': form})


@login_required
def read_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    if request.method == 'POST':
        form = AddUserToGroupForm(group=group, data=request.POST)
        if form.is_valid():
            group.user_set.add(form.cleaned_data['user'])
            group.save()
            messages.success(request, f'User has been added to the group {group.name}')
            return redirect('users:read_group', group_pk)
        else:
            messages.error(request, 'Try again')
    else:
        form = AddUserToGroupForm()
    return render(request, 'users_app/read_group.html', {'title': group.name,
                                                         'form': form,
                                                         'group': group,
                                                         'content': group.user_set.all()})


@login_required
def update_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    if request.method == 'POST':
        form = PostGroupForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            group.name = cd['name']
            group.customgroup.description = cd['description']
            group.customgroup.admin = cd['admin']
            group.customgroup.save()
            group.save()
            messages.success(request, 'Group has been changed')
            return redirect('users:groups')
        else:
            messages.error(request, 'Try again')
    else:
        form = PostGroupForm(instance=group.customgroup)
    return render(request, 'users_app/post_group.html', {'title': 'Update group',
                                                         'form': form})


@login_required
def delete_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    group.delete()
    messages.warning(request, 'Group has been removed')
    return redirect('users:groups')
