from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, date
from .models import Expense, Category, RecurringExpense, Income
from .forms import ExpenseForm, RecurringExpenseForm, IncomeForm, LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('kakeibo_app:expense_list')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username}さん、ようこそ！')
                return redirect('kakeibo_app:expense_list')
            else:
                messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
    else:
        form = LoginForm()
    
    return render(request, 'kakeibo_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'ログアウトしました。')
    return redirect('login')

@login_required
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')  # 日付の降順で表示
    categories = Category.objects.all()
    recurring_expenses = RecurringExpense.objects.all()
    incomes = Income.objects.all().order_by('-date')  # 日付の降順で表示
    return render(request, 'kakeibo_app/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
        'recurring_expenses': recurring_expenses,
        'incomes': incomes
    })

@login_required
def monthly_summary(request, year=None, month=None):
    # 年と月が指定されていない場合は現在の年月を使用
    if year is None or month is None:
        today = timezone.now().date()
        year = today.year
        month = today.month

    # 指定された年月の最初の日と最後の日を取得
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timezone.timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timezone.timedelta(days=1)

    # 収入の集計
    monthly_incomes = Income.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 支出の集計
    monthly_expenses = Expense.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    ).aggregate(total=Sum('amount'))['total'] or 0

    # カテゴリ別の支出集計
    category_expenses = Expense.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')

    # カテゴリー別支出の割合を計算
    for category in category_expenses:
        if monthly_expenses > 0:
            category['percentage'] = (category['total'] / monthly_expenses) * 100
        else:
            category['percentage'] = 0

    # 前月と翌月の年月を計算
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1

    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    return render(request, 'kakeibo_app/monthly_summary.html', {
        'year': year,
        'month': month,
        'monthly_incomes': monthly_incomes,
        'monthly_expenses': monthly_expenses,
        'balance': monthly_incomes - monthly_expenses,
        'category_expenses': category_expenses,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    })

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kakeibo_app:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'kakeibo_app/expense_form.html', {'form': form})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('kakeibo_app:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'kakeibo_app/expense_form.html', {'form': form})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('kakeibo_app:expense_list')
    return render(request, 'kakeibo_app/expense_confirm_delete.html', {'expense': expense})

@login_required
def recurring_expense_create(request):
    if request.method == 'POST':
        form = RecurringExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kakeibo_app:expense_list')
    else:
        form = RecurringExpenseForm()
    return render(request, 'kakeibo_app/recurring_expense_form.html', {'form': form})

@login_required
def recurring_expense_edit(request, pk):
    recurring_expense = get_object_or_404(RecurringExpense, pk=pk)
    if request.method == 'POST':
        form = RecurringExpenseForm(request.POST, instance=recurring_expense)
        if form.is_valid():
            form.save()
            return redirect('kakeibo_app:expense_list')
    else:
        form = RecurringExpenseForm(instance=recurring_expense)
    return render(request, 'kakeibo_app/recurring_expense_form.html', {'form': form})

@login_required
def recurring_expense_delete(request, pk):
    recurring_expense = get_object_or_404(RecurringExpense, pk=pk)
    if request.method == 'POST':
        recurring_expense.delete()
        return redirect('kakeibo_app:expense_list')
    return render(request, 'kakeibo_app/recurring_expense_confirm_delete.html', {'recurring_expense': recurring_expense})

@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kakeibo_app:expense_list')
    else:
        form = IncomeForm()
    return render(request, 'kakeibo_app/income_form.html', {'form': form})

@login_required
def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('kakeibo_app:expense_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'kakeibo_app/income_form.html', {'form': form})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        income.delete()
        return redirect('kakeibo_app:expense_list')
    return render(request, 'kakeibo_app/income_confirm_delete.html', {'income': income})

@login_required
def monthly_trend(request):
    # 過去12ヶ月分のデータを取得
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=365)
    
    # 月別の収入データを取得
    monthly_incomes = Income.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).annotate(
        year_month=TruncMonth('date')
    ).values('year_month').annotate(
        total=Sum('amount')
    ).order_by('year_month')

    # 月別の支出データを取得
    monthly_expenses = Expense.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).annotate(
        year_month=TruncMonth('date')
    ).values('year_month').annotate(
        total=Sum('amount')
    ).order_by('year_month')

    # データをグラフ用に整形
    months = []
    income_data = []
    expense_data = []
    balance_data = []

    # データを月ごとに整理
    current_date = start_date
    while current_date <= end_date:
        month_str = current_date.strftime('%Y-%m')
        months.append(month_str)
        
        # 収入データ
        income = next((item['total'] for item in monthly_incomes if item['year_month'].strftime('%Y-%m') == month_str), 0)
        income_data.append(income)
        
        # 支出データ
        expense = next((item['total'] for item in monthly_expenses if item['year_month'].strftime('%Y-%m') == month_str), 0)
        expense_data.append(expense)
        
        # 収支データ
        balance_data.append(income - expense)
        
        # 次の月へ
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

    return render(request, 'kakeibo_app/monthly_trend.html', {
        'months': months,
        'income_data': income_data,
        'expense_data': expense_data,
        'balance_data': balance_data,
    }) 