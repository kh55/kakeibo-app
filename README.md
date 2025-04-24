# 家計簿アプリ

Djangoで作成されたシンプルな家計簿管理アプリケーションです。支出と収入を管理し、月別の収支や推移を確認することができます。

## 機能

### 基本機能
- 支出の登録・編集・削除
- 収入の登録・編集・削除
- 定期支出の管理
- カテゴリー管理

### 分析機能
- 月別収支サマリー
  - 収入・支出・収支の表示
  - カテゴリー別支出の内訳
  - 前月・次月への移動
- 月別収支の推移グラフ
  - 過去12ヶ月分のデータ表示
  - 収入・支出・収支の推移
  - インタラクティブなグラフ表示

## 技術スタック
- Python 3.13
- Django 5.2
- Bootstrap 5.3
- Chart.js

## セットアップ

1. リポジトリをクローン
```bash
git clone git@github.com:kh55/kakeibo-app.git
cd kakeibo-app
```

2. 仮想環境を作成して有効化
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows
```

3. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

4. データベースのマイグレーション
```bash
cd kakeibo_project
python manage.py migrate
```

5. 開発サーバーを起動
```bash
python manage.py runserver
```

6. ブラウザでアクセス
```
http://localhost:8000/kakeibo/
```

## 今後の予定機能
- グラフの機能拡張
  - 期間選択機能
  - グラフの種類切り替え
  - データのエクスポート
- 予算管理機能
  - カテゴリーごとの予算設定
  - 予算に対する進捗状況の表示
- 年間収支の表示
  - 月別収支の年間サマリー
  - 年間のカテゴリー別支出分析 