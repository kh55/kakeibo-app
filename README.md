# 家計簿アプリ

Djangoで作成された家計簿管理アプリケーションです。

## 機能

- 支出の記録・編集・削除
- 収入の記録・編集・削除
- 定期支出の管理
- 月別収支サマリー
- 収支推移グラフ
- ログイン認証機能

## セットアップ

### 1. 環境変数の設定

ログイン認証機能を使用するために、`.env`ファイルを作成して環境変数を設定してください：

```bash
# .env ファイルを作成
cp env.example .env
```

`.env`ファイルを編集して、以下の設定を行ってください：

```env
# 管理者ユーザーの設定
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password

# Django設定
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**重要**: `.env`ファイルはGitにコミットされません。本番環境では必ず安全なパスワードを設定してください。

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. データベースのマイグレーション

```bash
python manage.py migrate
```

### 4. 管理者ユーザーの作成

```bash
python manage.py create_admin_user
```

### 5. 開発サーバーの起動

```bash
python manage.py runserver
```

## 使用方法

1. ブラウザで `http://localhost:8000/login/` にアクセス
2. 設定したユーザー名とパスワードでログイン
3. 家計簿の管理を開始

## デフォルト設定

環境変数が設定されていない場合のデフォルト値：
- ユーザー名: `admin`
- パスワード: `admin123`
- SECRET_KEY: `django-insecure-your-secret-key-here`
- DEBUG: `True`

**注意**: 本番環境では必ず`.env`ファイルで安全な設定を行ってください。

## 環境変数の説明

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `ADMIN_USERNAME` | 管理者ユーザー名 | `admin` |
| `ADMIN_PASSWORD` | 管理者パスワード | `admin123` |
| `SECRET_KEY` | Djangoの秘密鍵 | `django-insecure-your-secret-key-here` |
| `DEBUG` | デバッグモード | `True` |

## ファイル構成

```
kakeibo/
├── kakeibo_app/          # メインアプリケーション
│   ├── models.py         # データモデル
│   ├── views.py          # ビュー
│   ├── forms.py          # フォーム
│   ├── urls.py           # URL設定
│   └── management/       # 管理コマンド
├── kakeibo_project/      # プロジェクト設定
│   ├── settings.py       # 設定ファイル
│   └── urls.py           # メインURL設定
├── templates/            # テンプレート
├── static/               # 静的ファイル
├── .env                  # 環境変数（作成が必要）
├── env.example           # 環境変数の例
└── manage.py            # Django管理スクリプト
```

## トラブルシューティング

### .envファイルが読み込まれない場合

1. `.env`ファイルがプロジェクトのルートディレクトリにあることを確認
2. ファイル名が正確に`.env`であることを確認（`.env.txt`などになっていないか）
3. ファイルの内容が正しい形式であることを確認（`KEY=value`の形式）

### ログインできない場合

1. `python manage.py create_admin_user`を実行してユーザーを作成
2. `.env`ファイルの`ADMIN_USERNAME`と`ADMIN_PASSWORD`が正しく設定されているか確認
3. データベースが正しくマイグレーションされているか確認 