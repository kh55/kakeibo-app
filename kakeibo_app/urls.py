from django.urls import path
from . import views

app_name = 'kakeibo_app'

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('create/', views.expense_create, name='expense_create'),
    path('edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('recurring/create/', views.recurring_expense_create, name='recurring_expense_create'),
    path('recurring/edit/<int:pk>/', views.recurring_expense_edit, name='recurring_expense_edit'),
    path('recurring/delete/<int:pk>/', views.recurring_expense_delete, name='recurring_expense_delete'),
    path('income/create/', views.income_create, name='income_create'),
    path('income/edit/<int:pk>/', views.income_edit, name='income_edit'),
    path('income/delete/<int:pk>/', views.income_delete, name='income_delete'),
    path('monthly/<int:year>/<int:month>/', views.monthly_summary, name='monthly_summary'),
    path('monthly/', views.monthly_summary, name='monthly_summary_current'),
    path('trend/', views.monthly_trend, name='monthly_trend'),
] 