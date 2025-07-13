# さくらインターネットでのリバースプロキシ設定ガイド

## 概要

さくらインターネットの環境では、80番と443番ポートのみが利用可能です。Djangoアプリケーションを8000番ポートで動作させ、リバースプロキシを使用して80番ポートでアクセスできるようにする設定方法を説明します。

## 制限事項

### さくらインターネットのポート制限
- **利用可能ポート**: 80番（HTTP）、443番（HTTPS）のみ
- **制限されるポート**: 8000番などのカスタムポートは外部からアクセス不可
- **内部通信**: localhost:8000での内部通信は可能

## 解決方法

### 1. アーキテクチャ

```
外部アクセス → さくらインターネット（80番ポート） → リバースプロキシ → localhost:8000（Django）
```

### 2. 設定手順

#### ステップ1: さくらインターネットの管理画面でドメイン設定

1. **さくらインターネットの管理画面**にログイン
2. **ドメイン設定**または**サブドメイン設定**を選択
3. **新しいドメイン**または**サブドメイン**を追加

#### ステップ2: リバースプロキシ設定

さくらインターネットの管理画面で以下の設定を行います：

```
ドメイン: あなたのドメイン.sakura.ne.jp
ポート: 80
プロキシ先: localhost:8000
```

#### ステップ3: 設定確認

設定後、以下のURLでアクセスできるようになります：

- **ログインページ**: `http://あなたのドメイン/login/`
- **管理画面**: `http://あなたのドメイン/admin/`
- **家計簿アプリ**: `http://あなたのドメイン/kakeibo/`

## 代替案

### 1. さくらインターネットのVPSを使用

VPS環境では、より柔軟な設定が可能です：

```bash
# Nginxのインストール
pkg install nginx

# Nginx設定ファイルの作成
cat > /usr/local/etc/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name あなたのドメイン.sakura.ne.jp;
        
        location / {
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Nginxの起動
service nginx start
```

### 2. さくらインターネットのレンタルサーバーを使用

レンタルサーバー環境では、管理画面での設定が主な方法です：

1. **サブドメインの作成**
2. **リバースプロキシ設定**
3. **SSL証明書の設定**（必要に応じて）

## トラブルシューティング

### よくある問題

#### 1. リバースプロキシが動作しない
**症状**: 外部からアクセスできない
**解決方法**:
- さくらインターネットの管理画面で設定を確認
- Djangoアプリケーションが正常に動作しているか確認
- ログファイルでエラーを確認

#### 2. 静的ファイルが表示されない
**症状**: CSSやJavaScriptが読み込まれない
**解決方法**:
- `python manage.py collectstatic`を実行
- 静的ファイルのパス設定を確認
- WhiteNoiseの設定を確認

#### 3. セッションが保持されない
**症状**: ログイン後にセッションが切れる
**解決方法**:
- `SESSION_COOKIE_SECURE`設定を確認
- プロキシヘッダーの設定を確認

### デバッグ方法

#### 1. ログの確認
```bash
# Gunicornのログを確認
tail -f gunicorn.log
tail -f gunicorn-error.log

# システムログの確認
tail -f /var/log/messages
```

#### 2. プロセスの確認
```bash
# Gunicornプロセスの確認
ps aux | grep gunicorn

# ポートの確認
netstat -an | grep 8000
```

#### 3. 接続テスト
```bash
# ローカルでの接続テスト
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/login/

# 外部からの接続テスト
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://あなたのドメイン/login/
```

## セキュリティ考慮事項

### 1. ファイアウォール設定
- 80番と443番ポートのみを開放
- 8000番ポートは内部でのみ使用

### 2. SSL/TLS設定
- HTTPS（443番ポート）の使用を推奨
- Let's Encryptなどの無料SSL証明書の利用

### 3. ヘッダー設定
- プロキシヘッダーの適切な設定
- セキュリティヘッダーの追加

## パフォーマンス最適化

### 1. キャッシュ設定
- 静的ファイルのキャッシュ
- データベースクエリの最適化

### 2. 圧縮設定
- gzip圧縮の有効化
- 画像の最適化

### 3. ロードバランシング
- 複数ワーカーの設定
- 負荷分散の実装

## 設定例

### さくらインターネット管理画面での設定例

```
ドメイン設定:
- ドメイン名: kakeibo.yourdomain.sakura.ne.jp
- ポート: 80
- プロキシ先: localhost:8000
- SSL: 有効（推奨）

サブドメイン設定:
- サブドメイン: app
- メインドメイン: yourdomain.sakura.ne.jp
- ポート: 80
- プロキシ先: localhost:8000
```

### アクセスURL例

設定後、以下のURLでアクセスできます：

```
http://kakeibo.yourdomain.sakura.ne.jp/login/
http://app.yourdomain.sakura.ne.jp/admin/
https://kakeibo.yourdomain.sakura.ne.jp/kakeibo/  # SSL使用時
```

## まとめ

さくらインターネットの環境制限に対応するため、リバースプロキシを使用して80番ポートでアクセスできるように設定しました。この方法により、Djangoアプリケーションを正常に動作させながら、外部からのアクセスも可能になります。

### 重要なポイント

1. **ポート制限の理解**: 80番と443番ポートのみ利用可能
2. **内部通信の活用**: localhost:8000での内部通信を活用
3. **管理画面での設定**: さくらインターネットの管理画面での設定が重要
4. **セキュリティの確保**: 適切なセキュリティ設定の実装

---

*このガイドはさくらインターネットの環境制限に対応するための設定方法を説明しています。実際の設定は環境やプランによって異なる場合があります。* 