from django.core.management.base import BaseCommand
from django.utils import timezone
from kakeibo_app.models import RecurringExpense

class Command(BaseCommand):
    help = '定期支出から支出を生成する'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            help='生成する支出の日付（YYYY-MM-DD形式）',
        )

    def handle(self, *args, **options):
        target_date = None
        if options['date']:
            try:
                target_date = timezone.datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('日付の形式が正しくありません。YYYY-MM-DD形式で指定してください。'))
                return

        generated_expenses = RecurringExpense.generate_all_expenses(target_date)
        
        if generated_expenses:
            self.stdout.write(self.style.SUCCESS(f'{len(generated_expenses)}件の支出を生成しました。'))
            for expense in generated_expenses:
                self.stdout.write(f'- {expense.date}: {expense.amount}円 ({expense.card})')
        else:
            self.stdout.write(self.style.SUCCESS('生成する支出はありませんでした。')) 