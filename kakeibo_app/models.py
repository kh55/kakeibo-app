from django.db import models
from django.utils import timezone
from datetime import datetime, date

class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=100)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField('カード名', max_length=100)
    number = models.CharField('カード番号', max_length=16)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.number})"

class Income(models.Model):
    date = models.DateField('日付')
    amount = models.IntegerField('金額')
    memo = models.TextField('メモ', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.amount}円"

class Expense(models.Model):
    date = models.DateField('日付')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    amount = models.IntegerField('金額')
    card = models.ForeignKey(Card, on_delete=models.PROTECT, verbose_name='カード', null=True, blank=True)
    memo = models.TextField('メモ', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.category} - {self.amount}円"

class RecurringExpense(models.Model):
    DAY_CHOICES = [
        (1, '1日'),
        (2, '2日'),
        (3, '3日'),
        (4, '4日'),
        (5, '5日'),
        (6, '6日'),
        (7, '7日'),
        (8, '8日'),
        (9, '9日'),
        (10, '10日'),
        (11, '11日'),
        (12, '12日'),
        (13, '13日'),
        (14, '14日'),
        (15, '15日'),
        (16, '16日'),
        (17, '17日'),
        (18, '18日'),
        (19, '19日'),
        (20, '20日'),
        (21, '21日'),
        (22, '22日'),
        (23, '23日'),
        (24, '24日'),
        (25, '25日'),
        (26, '26日'),
        (27, '27日'),
        (28, '28日'),
        (29, '29日'),
        (30, '30日'),
        (31, '31日'),
    ]

    day = models.IntegerField('支払日', choices=DAY_CHOICES)
    amount = models.IntegerField('金額')
    card = models.ForeignKey(Card, on_delete=models.PROTECT, verbose_name='カード')
    start_date = models.DateField('開始日')
    end_date = models.DateField('終了日', null=True, blank=True)
    memo = models.TextField('メモ', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f"{self.day}日 - {self.amount}円 - {self.card}"

    def generate_expense(self, target_date=None):
        """
        定期支出から支出を生成する
        """
        if target_date is None:
            target_date = timezone.now().date()

        # 対象日が開始日より前の場合は生成しない
        if target_date < self.start_date:
            return None

        # 終了日が設定されており、対象日が終了日より後の場合は生成しない
        if self.end_date and target_date > self.end_date:
            return None

        # 対象日の日付が支払日と一致しない場合は生成しない
        if target_date.day != self.day:
            return None

        # 既に同じ日付の支出が存在する場合は生成しない
        if Expense.objects.filter(date=target_date, card=self.card, amount=self.amount).exists():
            return None

        # 支出を生成
        expense = Expense.objects.create(
            date=target_date,
            category=self.category if hasattr(self, 'category') else None,
            amount=self.amount,
            card=self.card,
            memo=f"定期支出: {self.memo}" if self.memo else "定期支出"
        )
        return expense

    @classmethod
    def generate_all_expenses(cls, target_date=None):
        """
        すべての定期支出から支出を生成する
        """
        if target_date is None:
            target_date = timezone.now().date()

        generated_expenses = []
        for recurring_expense in cls.objects.all():
            expense = recurring_expense.generate_expense(target_date)
            if expense:
                generated_expenses.append(expense)
        return generated_expenses 