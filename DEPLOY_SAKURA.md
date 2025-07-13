# さくらインターネットへのデプロイ手順

このドキュメントでは、GitHub Actionsを使用してさくらインターネットのレンタルサーバーにDjangoアプリケーションをデプロイする手順を説明します。

## 前提条件

1. さくらインターネットのレンタルサーバーアカウント
2. GitHubリポジトリ
3. さくらインターネットでSSH接続が有効になっていること

## セットアップ手順

### 1. GitHub Secretsの設定

GitHubリポジトリの設定画面で以下のSecretsを設定してください：

- `SAKURA_HOST`: さくらインターネットのサーバーホスト名
- `SAKURA_USERNAME`: さくらインターネットのユーザー名
- `SAKURA_PASSWORD`: さくらインターネットのパスワード
- `SAKURA_PORT`: さくらインターネットのSSHポート（通常は22）
- `SAKURA_DEPLOY_PATH`: デプロイ先のパス（オプション、デフォルトは `/home/ユーザー名/`）

#### デプロイパスの設定例：
- ホームディレクトリ: `/home/username/` （デフォルト）
- Webディレクトリ: `/var/www/`
- カスタムパス: `/home/username/webapps/kakeibo/`

### 2. 環境変数の設定

さくらインターネットのサーバー上で以下の手順を実行してください：

```bash
# デプロイ先ディレクトリに移動（SAKURA_DEPLOY_PATHで指定したパス）
# 例: /home/username/ または /var/www/ など
cd $SAKURA_DEPLOY_PATH

# プロジェクトディレクトリを作成
mkdir kakeibo
cd kakeibo

# 環境変数ファイルを作成
cp env.sakura.example .env

# .envファイルを編集して実際の値を設定
nano .env
```

`.env`ファイルの内容例：
```env
SECRET_KEY=your-actual-secret-key-here
DEBUG=False
DOMAIN=your-domain.sakura.ne.jp
DATABASE_URL=sqlite:///db.sqlite3
STATIC_URL=/static/
STATIC_ROOT=staticfiles
LOG_LEVEL=INFO
ALLOWED_HOSTS=localhost,127.0.0.1,.sakura.ne.jp,your-domain.sakura.ne.jp
TIME_ZONE=Asia/Tokyo
LANGUAGE_CODE=ja
```

### 3. ログディレクトリの作成

```bash
mkdir logs
```

### 4. 静的ファイルディレクトリの作成

```bash
mkdir staticfiles
```

## デプロイの実行

### 自動デプロイ

mainブランチにプッシュすると自動的にデプロイが実行されます。

### 手動デプロイ

GitHubのActionsタブから「Deploy to Sakura Internet」ワークフローを手動で実行できます。

## デプロイ後の確認

### 1. プロセスの確認

```bash
ps aux | grep gunicorn
```

### 2. ログの確認

```bash
tail -f kakeibo.log
```

### 3. アプリケーションの動作確認

ブラウザで `https://your-domain.sakura.ne.jp` にアクセスしてアプリケーションが正常に動作することを確認してください。

## トラブルシューティング

### よくある問題と解決方法

#### 1. ポートが使用中の場合

```bash
# 使用中のポートを確認
netstat -tlnp | grep :8000

# プロセスを停止（デプロイパスに応じて調整）
kill $(cat $SAKURA_DEPLOY_PATH/kakeibo.pid)
```

#### 2. 権限エラーの場合

```bash
# ファイルの権限を確認
ls -la

# 必要に応じて権限を変更
chmod 755 kakeibo
chmod 644 kakeibo/.env
```

#### 3. データベースエラーの場合

```bash
cd kakeibo
source venv/bin/activate
python manage.py migrate
```

#### 4. 静的ファイルが表示されない場合

```bash
cd kakeibo
source venv/bin/activate
python manage.py collectstatic --noinput
```

## セキュリティに関する注意事項

1. `.env`ファイルには機密情報が含まれているため、Gitにコミットしないでください
2. `SECRET_KEY`は強力なランダム文字列を使用してください
3. 本番環境では`DEBUG=False`に設定してください
4. 定期的にセキュリティアップデートを適用してください

## バックアップ

デプロイ前に自動的にバックアップが作成されます。手動でバックアップを作成する場合：

```bash
# データベースのバックアップ
cp $SAKURA_DEPLOY_PATH/kakeibo/db.sqlite3 $SAKURA_DEPLOY_PATH/kakeibo/db.sqlite3.backup

# ファイル全体のバックアップ
tar -czf kakeibo_backup_$(date +%Y%m%d_%H%M%S).tar.gz $SAKURA_DEPLOY_PATH/kakeibo/
```

## サポート

問題が発生した場合は、以下の情報を確認してください：

1. GitHub Actionsのログ
2. さくらインターネットのサーバーログ
3. アプリケーションのログ（`kakeibo.log`） 