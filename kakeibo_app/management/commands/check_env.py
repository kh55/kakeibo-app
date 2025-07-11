from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = '環境変数の設定を確認します'

    def handle(self, *args, **options):
        self.stdout.write('=== 環境変数の確認 ===')
        
        # 管理者ユーザー設定
        self.stdout.write(f'ADMIN_USERNAME: {settings.ADMIN_USERNAME}')
        self.stdout.write(f'ADMIN_PASSWORD: {"*" * len(settings.ADMIN_PASSWORD)} (長さ: {len(settings.ADMIN_PASSWORD)})')
        
        # Django設定
        self.stdout.write(f'SECRET_KEY: {settings.SECRET_KEY[:20]}... (長さ: {len(settings.SECRET_KEY)})')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        
        # ログイン設定
        self.stdout.write(f'LOGIN_URL: {settings.LOGIN_URL}')
        self.stdout.write(f'LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}')
        self.stdout.write(f'LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}')
        
        self.stdout.write(self.style.SUCCESS('環境変数の確認が完了しました')) 