from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('categories/', views.read_categories, name='categories'),
    path('categories/post_category/', views.post_category, name='post_category'),
    path('categories/<int:category_pk>/update_category/', views.update_category, name='update_category'),
    path('categories/<int:category_pk>/delete_category/', views.delete_category, name='delete_category'),
    path('categories/<int:category_pk>/expenses', views.read_expenses_by_category, name='read_expenses_by_category'),
    path('receipts/', views.read_receipts, name='receipts'),
    path('receipts/post_receipt/', views.post_receipt, name='post_receipt'),
    path('receipts/<int:receipt_pk>/update_receipt/', views.update_receipt, name='update_receipt'),
    path('receipts/<int:receipt_pk>/delete_receipt/', views.delete_receipt, name='delete_receipt'),
    path('receipts/<int:receipt_pk>/', views.read_receipt, name='read_receipt'),
    path('receipts/<int:receipt_pk>/expenses/post_expense/', views.post_expense, name='post_expense'),
    path('receipts/<int:receipt_pk>/expenses/<int:expense_pk>/update_expense/', views.update_expense,
         name='update_expense'),
    path('receipts/<int:receipt_pk>/expenses/<int:expense_pk>/delete_expense/', views.delete_expense,
         name='delete_expense'),
    path('statistics/personal/', views.personal_statistics, name='personal_statistics'),
    path('statistics/groups/', views.statistics_groups, name='statistics_groups'),
    path('statistics/groups/<int:group_pk>/', views.group_statistics, name='group_statistics'),
]
