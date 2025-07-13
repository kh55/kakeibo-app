# 技術詳細とトラブルシューティング

## ワークフローファイルの詳細

### 完全なワークフローファイル

```yaml
name: Deploy to Sakura Internet

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
    
    - name: Deploy
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SAKURA_HOST }}
        username: ${{ secrets.SAKURA_USERNAME }}
        password: ${{ secrets.SAKURA_PASSWORD }}
        script: |
          cd ${{ secrets.SAKURA_DEPLOY_PATH }}
          git pull origin main
          
          # 段階1: 環境確認
          echo "=== 環境確認 ==="
          echo "Python version:"
          python3 --version || echo "Python3 not found"
          echo "Python path:"
          which python3
          echo "Python modules:"
          python3 -c "import sys; print('\\n'.join(sys.path))"
          echo "Pip version:"
          python3 -m pip --version || echo "Pip not found"
          echo "Pkg available:"
          pkg --version || echo "pkg not available"
          echo "Current directory:"
          pwd
          echo "Directory contents:"
          ls -la
          echo "=================="
          
          # 段階2: pipのインストール
          echo "=== pipインストール ==="
          echo "Python 3.8用のget-pip.pyをダウンロード:"
          curl -s https://bootstrap.pypa.io/pip/3.8/get-pip.py -o get-pip.py || echo "get-pip.py download failed"
          echo "pipをインストール:"
          python3 get-pip.py --user || echo "pip install failed"
          echo "pipの確認:"
          python3 -m pip --version || echo "pip not found"
          echo "====================="
          
          # 段階3: 仮想環境の確認・作成
          echo "=== 仮想環境確認 ==="
          echo "仮想環境の存在確認..."
          ls -la | grep venv || echo "venvディレクトリが見つかりません"
          
          echo "仮想環境を作成します..."
          python3 -m venv venv
          echo "仮想環境を作成しました"
          
          echo "仮想環境をアクティベート..."
          source venv/bin/activate
          echo "アクティベート後のPython:"
          python --version
          echo "アクティベート後のPip:"
          python -m pip --version
          echo "====================="
          
          # 段階4: 依存関係のインストール
          echo "=== 依存関係インストール ==="
          echo "requirements.txtの内容確認:"
          cat requirements.txt
          echo "依存関係をインストール:"
          python -m pip install -r requirements.txt || echo "依存関係のインストールに失敗"
          echo "インストールされたパッケージ:"
          python -m pip list
          echo "====================="
          
          # 段階5: Django設定とマイグレーション
          echo "=== Django設定とマイグレーション ==="
          echo "Djangoのバージョン確認:"
          python -m django --version
          echo "データベースマイグレーション:"
          python manage.py migrate || echo "マイグレーションに失敗"
          echo "静的ファイルの収集:"
          python manage.py collectstatic --noinput || echo "静的ファイル収集に失敗"
          echo "Django設定の確認:"
          python manage.py check || echo "Django設定に問題があります"
          echo "====================="
          
          # 段階6: アプリケーション起動
          echo "=== アプリケーション起動 ==="
          echo "現在のプロセス確認:"
          ps aux | grep gunicorn || echo "Gunicornプロセスなし"
          echo "Gunicornの起動テスト:"
          timeout 10s python -m gunicorn kakeibo_project.wsgi:application --bind 0.0.0.0:8000 --workers 1 || echo "Gunicorn起動テスト完了"
          echo "ポート8000の確認:"
          sockstat -l | grep 8000 || echo "ポート8000でリッスンしていません"
          echo "====================="
          
          # 段階7: 本番環境設定
          echo "=== 本番環境設定 ==="
          echo "環境変数ファイルの確認:"
          ls -la .env* || echo "環境変数ファイルが見つかりません"
          echo "本番環境用の環境変数を設定:"
          export DEBUG=False
          export SECRET_KEY="django-insecure-production-secret-key-change-this"
          export ALLOWED_HOSTS="localhost,127.0.0.1,あなたのドメイン.sakura.ne.jp"
          echo "本番環境用の設定確認:"
          echo "DEBUG設定:"
          python -c "from kakeibo_project.settings import DEBUG; print(f'DEBUG: {DEBUG}')" || echo "設定確認に失敗"
          echo "ALLOWED_HOSTS設定:"
          python -c "from kakeibo_project.settings import ALLOWED_HOSTS; print(f'ALLOWED_HOSTS: {ALLOWED_HOSTS}')" || echo "設定確認に失敗"
          echo "管理者ユーザーの作成:"
          python manage.py create_admin_user || echo "管理者ユーザー作成に失敗"
          echo "====================="
          
          # 段階8: アプリケーション起動と動作確認
          echo "=== アプリケーション起動と動作確認 ==="
          echo "既存のGunicornプロセスを停止:"
          pkill -f gunicorn || echo "停止するプロセスなし"
          echo "Gunicornをバックグラウンドで起動（本番環境用）:"
          nohup python -m gunicorn kakeibo_project.wsgi:application --bind 0.0.0.0:8000 --workers 1 --daemon --access-logfile gunicorn.log --error-logfile gunicorn-error.log || echo "Gunicorn起動に失敗"
          echo "3秒待機..."
          sleep 3
          echo "Gunicornプロセスの確認:"
          ps aux | grep gunicorn
          echo "ログファイルの確認:"
          ls -la gunicorn*.log || echo "ログファイルが見つかりません"
          echo "動作確認（curl）:"
          echo "ローカルアクセス確認:"
          curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/login/ || echo "curlでアクセスできません"
          echo "====================="
          
          # 段階9: デプロイメント完了とアクセス方法
          echo "=== デプロイメント完了 ==="
          echo "🎉 さくらインターネットでのデプロイメントが完了しました！"
          echo ""
          echo "📋 次のステップ:"
          echo "1. さくらインターネットの管理画面でドメイン設定"
          echo "2. サブドメインまたはドメインを追加"
          echo "3. ポート8000へのアクセス設定"
          echo ""
          echo "🌐 アクセス方法:"
          echo "- ログインページ: http://あなたのドメイン:8000/login/"
          echo "- 管理画面: http://あなたのドメイン:8000/admin/"
          echo "- 家計簿アプリ: http://あなたのドメイン:8000/kakeibo/"
          echo ""
          echo "🔧 管理者アカウント:"
          echo "- ユーザー名: admin"
          echo "- パスワード: secure_password_123"
          echo ""
          echo "⚠️  注意事項:"
          echo "- 本番環境ではSECRET_KEYを変更してください"
          echo "- パスワードを強力なものに変更してください"
          echo "- ファイアウォールで8000番ポートを開放してください"
          echo "====================="
```

## 主要な技術的ポイント

### 1. SSH接続の設定

#### GitHub Secretsの設定
```bash
SAKURA_HOST: サーバーのIPアドレスまたはホスト名
SAKURA_USERNAME: SSHユーザー名
SAKURA_PASSWORD: SSHパスワード
SAKURA_DEPLOY_PATH: デプロイ先のディレクトリパス
```

#### 認証方式の選択
- **パスワード認証**: 簡単だがセキュリティリスク
- **SSH鍵認証**: 推奨（より安全）

### 2. Python環境の構築

#### pipのインストール方法
```bash
# Python 3.8専用のget-pip.pyを使用
curl -s https://bootstrap.pypa.io/pip/3.8/get-pip.py -o get-pip.py
python3 get-pip.py --user
```

#### 仮想環境の作成
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Django設定の最適化

#### 本番環境用の設定
```python
DEBUG = False
SECRET_KEY = "your-secure-secret-key"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "your-domain.sakura.ne.jp"]
```

#### 静的ファイルの設定
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. Gunicornの設定

#### 基本的な起動コマンド
```bash
python -m gunicorn kakeibo_project.wsgi:application --bind 0.0.0.0:8000 --workers 1
```

#### 本番環境用の設定
```bash
nohup python -m gunicorn kakeibo_project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --daemon \
  --access-logfile gunicorn.log \
  --error-logfile gunicorn-error.log
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. pipのインストールエラー
**問題**: `No module named pip`
**解決方法**: Python 3.8専用のget-pip.pyを使用

#### 2. 権限エラー
**問題**: `Permission denied`
**解決方法**: `--user`オプションでユーザーディレクトリにインストール

#### 3. ポート確認エラー
**問題**: `sockstat`や`netstat`が使えない
**解決方法**: `curl`でHTTPリクエストを送信して動作確認

#### 4. 静的ファイルエラー
**問題**: `STATICFILES_DIRS`のディレクトリが存在しない
**解決方法**: 警告レベルなので無視可能、またはディレクトリを作成

#### 5. 環境変数の読み込みエラー
**問題**: `.env`ファイルが読み込まれない
**解決方法**: ワークフロー内で直接環境変数を設定

### デバッグ方法

#### 1. ログの確認
```bash
# Gunicornのログを確認
tail -f gunicorn.log
tail -f gunicorn-error.log
```

#### 2. プロセスの確認
```bash
# Gunicornプロセスの確認
ps aux | grep gunicorn
```

#### 3. ポートの確認
```bash
# 代替的なポート確認方法
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/
```

## セキュリティ考慮事項

### 1. 環境変数の管理
- 機密情報はGitHub Secretsで管理
- 本番環境では強力なSECRET_KEYを使用

### 2. ファイアウォール設定
- 必要最小限のポートのみ開放
- 特定のIPアドレスからのアクセス制限を検討

### 3. アプリケーションのセキュリティ
- DEBUGモードを無効化
- 適切なALLOWED_HOSTS設定
- HTTPSの使用を推奨

## パフォーマンス最適化

### 1. Gunicornの設定
- ワーカー数の調整（CPUコア数 × 2 + 1）
- タイムアウト設定の最適化

### 2. 静的ファイルの配信
- WhiteNoiseを使用した効率的な配信
- 圧縮とキャッシュの活用

### 3. データベースの最適化
- インデックスの適切な設定
- クエリの最適化

## 監視とメンテナンス

### 1. ログ監視
- アクセスログとエラーログの定期確認
- 異常なアクセスパターンの検出

### 2. パフォーマンス監視
- レスポンスタイムの監視
- リソース使用量の確認

### 3. セキュリティ監視
- 不正アクセスの検出
- 脆弱性の定期的な確認

---

*このドキュメントは実際の運用経験に基づいて作成されています。環境や要件に応じて適宜調整してください。* 