from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Expense, Category, RecurringExpense, Income

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='ユーザー名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ユーザー名を入力してください'})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワードを入力してください'})
    )

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'card', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        }

class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ['day', 'amount', 'card', 'start_date', 'end_date', 'memo']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'amount', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        } 