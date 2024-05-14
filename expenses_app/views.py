from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from expenses_app.forms import (PostCategoryForm, PostExpenseForm,
                                PostReceiptForm, DateFromToForm)
from expenses_app.models import Category, Receipt, Expense
from django.contrib.auth.models import Group


def index(request):
    return render(request, 'expenses_app/index.html', {'title': 'Main Page'})


def about(request):
    return render(request, 'expenses_app/about.html', {'title': 'About us',
                                                       'content': 'ABOUT'})


def read_categories(request):
    user = request.user
    content = Category.objects.filter(user=user.pk)
    return render(request, 'expenses_app/categories.html', {'title': 'Categories',
                                                            'content': content})


def post_category(request):
    if request.method == 'POST':
        form = PostCategoryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_cat = Category(user=request.user,
                               title=cd['title'],
                               usefulness=cd['usefulness'],
                               color=cd['color'])
            new_cat.save()
            messages.success(request, 'Category has been added')
            return redirect('expenses:post_category')
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostCategoryForm()
    return render(request, 'expenses_app/post_category.html', {'title': 'Post category',
                                                               'form': form})


def update_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    if request.method == 'POST':
        form = PostCategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            category.user = request.user
            category.title = cd['title']
            category.usefulness = cd['usefulness']
            category.color = cd['color']
            category.save()
            messages.success(request, 'Category has been changed successfully')
            return redirect('expenses:categories')
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostCategoryForm(instance=category)
    return render(request, 'expenses_app/post_category.html', {'title': 'Update category',
                                                               'form': form})


def delete_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    category.delete()
    messages.warning(request, 'Category has been removed')
    return redirect('expenses:categories')


def read_expenses_by_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    time_filters = dict()
    form = None
    if request.method == 'POST':
        form = DateFromToForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            time_filters = {'receipt__purchase_time__gte': cd['date_from'],
                            'receipt__purchase_time__lte': cd['date_to']}
    if not form:
        form = DateFromToForm()
    filter_by_category = {'category': category, **time_filters}
    content = Expense.objects.filter(**filter_by_category).order_by('receipt__purchase_time')
    return render(request, 'expenses_app/read_expenses_by_category.html', {'title': f'{category} expenses',
                                                                           'content': content,
                                                                           'form': form})


def read_receipts(request):
    user = request.user
    content = Receipt.objects.filter(user=user.pk).order_by('-purchase_time')
    for receipt in content:
        receipt.purchase_time = receipt.purchase_time.strftime("%d.%m.%Y - %H:%M")
        receipt.total_cost = sum(map(lambda x: x.cost, receipt.expense_set.all()))
    return render(request, 'expenses_app/receipts.html', {'title': 'Receipts',
                                                          'content': content})


def post_receipt(request):
    if request.method == 'POST':
        form = PostReceiptForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_receipt = Receipt(title=cd['title'],
                                  user=request.user,
                                  purchase_time=cd['purchase_time'])
            new_receipt.save()
            messages.success(request, 'Receipt has been added')
            return redirect('expenses:post_receipt')
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostReceiptForm()
    return render(request, 'expenses_app/post_receipt.html', {'title': 'Post receipt',
                                                              'form': form})


def update_receipt(request, receipt_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)
    if request.method == 'POST':
        form = PostReceiptForm(instance=receipt, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receipt has been changed successfully')
            return redirect('expenses:receipts')
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostReceiptForm(instance=receipt)
    return render(request, 'expenses_app/post_receipt.html', {'title': 'Update receipt',
                                                              'form': form})


def delete_receipt(request, receipt_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)
    receipt.delete()
    messages.warning(request, 'Receipt has been removed')
    return redirect('expenses:receipts')


def read_receipt(request, receipt_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)
    expenses = receipt.expense_set.all()
    return render(request, 'expenses_app/read_receipt.html', {'title': 'Receipt expenses',
                                                              'content': expenses,
                                                              'receipt': receipt})


def post_expense(request, receipt_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)
    if request.method == 'POST':
        form = PostExpenseForm(user=request.user, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_expense = Expense(title=cd['title'],
                                  category=cd['category'],
                                  cost=cd['cost'],
                                  receipt=receipt)
            new_expense.save()
            messages.success(request, 'Expense has been added')
            return redirect('expenses:post_expense', receipt_pk=receipt_pk)
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostExpenseForm(user=request.user)
    return render(request, 'expenses_app/post_expense.html', {'title': 'Post expense',
                                                              'form': form,
                                                              'receipt': receipt})


def update_expense(request, receipt_pk, expense_pk):
    receipt = get_object_or_404(Receipt, pk=receipt_pk)
    expense = get_object_or_404(Expense, pk=expense_pk)
    if request.method == 'POST':
        form = PostExpenseForm(user=request.user, instance=expense, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense has been changed successfully')
            return redirect('expenses:read_receipt', receipt_pk)
        else:
            messages.error(request, 'Try again', extra_tags='danger')
    else:
        form = PostExpenseForm(user=request.user, instance=expense)
    return render(request, 'expenses_app/post_expense.html', {'title': 'Update expense',
                                                              'form': form,
                                                              'receipt': receipt})


def delete_expense(request, receipt_pk, expense_pk):
    expense = get_object_or_404(Expense, pk=expense_pk)
    expense.delete()
    messages.warning(request, 'Expense has been removed')
    return redirect('expenses:read_receipt', receipt_pk)


def statistics_groups(request):
    user = request.user
    return render(request, 'expenses_app/statistics_groups.html', {'title': 'Groups',
                                                                   'content': user.groups.all()})


def get_personal_statistics(user, time_filters):
    def count_query_sum(custom_filter):
        return sum(map(lambda x: x.cost, Expense.objects.filter(**custom_filter)))
    categories = Category.objects.filter(user=user)
    categories_info = dict()

    filter_by_user = {'receipt__user': user, **time_filters}
    user_total_cost = count_query_sum(filter_by_user)

    if user_total_cost:
        for category in categories:
            categories_info[category.title] = dict()
            categories_info[category.title]['color'] = category.color
            filter_by_category = {'category': category, **time_filters}
            categories_info[category.title]['category_total_cost'] = count_query_sum(filter_by_category)
            categories_info[category.title]['category_percentage'] = \
                round((categories_info[category.title]['category_total_cost'] / user_total_cost) * 100, 2)
    categories_info = dict(sorted(categories_info.items(), key=lambda x: x[1]['category_total_cost'], reverse=True))
    return {'user_total_cost': user_total_cost, 'categories_info': categories_info}


def personal_statistics(request):
    time_filters = dict()
    form = None

    if request.method == 'POST':
        form = DateFromToForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            time_filters = {'receipt__purchase_time__gte': cd['date_from'],
                            'receipt__purchase_time__lte': cd['date_to']}
    if not form:
        form = DateFromToForm()
    content = get_personal_statistics(request.user, time_filters)
    return render(request, 'expenses_app/personal_statistics.html', {'title': 'Personal statistics',
                                                                     'form': form,
                                                                     'content': content})


def group_statistics(request, group_pk):
    time_filters = dict()
    form = None
    group = get_object_or_404(Group, pk=group_pk)
    users = group.user_set.all()
    users_info = dict()

    if request.method == 'POST':
        form = DateFromToForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            time_filters = {'receipt__purchase_time__gte': cd['date_from'],
                            'receipt__purchase_time__lte': cd['date_to']}
    if not form:
        form = DateFromToForm()
    for user in users:
        users_info[user.username] = get_personal_statistics(user, time_filters)
    group_total_cost = sum(map(lambda x: x['user_total_cost'], users_info.values()))
    users_info = dict(sorted(users_info.items(), key=lambda x: x[1]['user_total_cost'], reverse=True))
    return render(request, 'expenses_app/group_statistics.html', {'title': 'Personal statistics',
                                                                  'form': form,
                                                                  'group_total_cost': group_total_cost,
                                                                  'users_info': users_info})
