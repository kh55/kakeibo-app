# さくらインターネット Django デプロイメント ドキュメント

このディレクトリには、さくらインターネットのFreeBSD環境でDjangoアプリケーションを自動デプロイメントするための詳細なドキュメントが含まれています。

## ドキュメント構成

### 📖 [sakura-deployment-guide.md](./sakura-deployment-guide.md)
**メインガイド** - デプロイメントの全体手順と学び

- 段階的な対応手順の詳細
- つまづいたポイントと解決方法
- 調査した内容と得た気づき
- 重要な学びと次のステップ

### 🔧 [technical-details.md](./technical-details.md)
**技術詳細** - 実装の詳細とトラブルシューティング

- 完全なワークフローファイル
- 主要な技術的ポイント
- トラブルシューティングガイド
- セキュリティとパフォーマンスの考慮事項

## クイックスタート

1. **GitHub Secretsの設定**
   ```bash
   SAKURA_HOST: サーバーのIPアドレス
   SAKURA_USERNAME: SSHユーザー名
   SAKURA_PASSWORD: SSHパスワード
   SAKURA_DEPLOY_PATH: デプロイ先ディレクトリ
   ```

2. **ワークフローファイルの配置**
   `.github/workflows/deploy-sakura.yml` を作成

3. **デプロイメントの実行**
   GitHubでmainブランチにプッシュするか、手動でワークフローを実行

## 対応環境

- **ホスティング**: さくらインターネット（FreeBSD 13.0）
- **Python**: 3.8.12
- **Django**: 4.2.10
- **Webサーバー**: Gunicorn 21.2.0

## 主な特徴

### ✅ 段階的なアプローチ
- 最小限の機能から始めて段階的に改善
- 各段階での動作確認とエラーハンドリング

### ✅ 環境固有の対応
- さくらインターネットのFreeBSD環境に最適化
- 権限制限やコマンド制限への代替手段

### ✅ セキュリティと運用性
- 本番環境での適切なセキュリティ設定
- 自動化による運用効率の向上

## トラブルシューティング

よくある問題と解決方法は [technical-details.md](./technical-details.md) の「トラブルシューティング」セクションを参照してください。

## 参考資料

- [Vultr: How to Install Python and Pip on FreeBSD 14.0](https://docs.vultr.com/how-to-install-python-and-pip-on-freebsd-14-0)
- [FreeBSD Forums: Python Modules Installation](https://forums.freebsd.org/threads/how-to-properly-install-and-use-python-modules-in-freebsd.83216/)
- [TEAM T3A: さくらのVPSでCentOS7のポートを開放する](https://www.t3a.jp/blog/infrastructure/centos-port-open/)

## ライセンス

このドキュメントは実際のデプロイメント経験に基づいて作成されています。自由にご利用ください。

---

**注意**: このドキュメントは特定の環境での経験に基づいています。お使いの環境や要件に応じて適宜調整してください。 