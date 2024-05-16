from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages

from .forms import LoginUserForm, RegisterUserForm, PostGroupForm, AddUserToGroupForm, UpdateUserForm
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


def account(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been changed')
            return redirect('users:account')
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'users_app/account.html', {'title': 'My account',
                                                      'form': form})


def read_groups(request):
    user = request.user
    return render(request, 'users_app/groups.html', {'title': 'Groups',
                                                     'content': user.groups.all()})


def post_group(request):
    if request.method == 'POST':
        form = PostGroupForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_group = Group(name=cd['name'])
            new_group.save()
            new_group.user_set.add(request.user)
            new_group.save()
            new_cust_group = CustomGroup(group=new_group,
                                         description=cd['description'],
                                         admin=cd['admin'])
            new_cust_group.save()
            messages.success(request, 'Group has been added')

        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostGroupForm()
    return render(request, 'users_app/post_group.html', {'title': 'Post group',
                                                         'form': form})


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
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = AddUserToGroupForm()
    return render(request, 'users_app/read_group.html', {'title': group.name,
                                                         'form': form,
                                                         'group': group,
                                                         'content': group.user_set.all()})


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
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostGroupForm(instance=group.customgroup)
    return render(request, 'users_app/post_group.html', {'title': 'Update group',
                                                         'form': form})


def delete_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    group.delete()
    messages.warning(request, 'Group has been removed')
    return redirect('users:groups')
