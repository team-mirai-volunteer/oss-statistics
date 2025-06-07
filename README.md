# OSS統計ダッシュボード

Team Mirai Volunteer組織の全パブリックリポジトリの統計情報を収集・可視化するダッシュボードです。開発祭りの盛り上げ演出として、コミット数、PR数、貢献者数などを美しいUIで表示します。

## 機能

### 📊 統計情報収集
- **活動量**: コミット数、PR数、Issue数
- **参加者**: 貢献者総数、新規参加者数
- **品質**: CI成功率、レビュー状況
- **コード**: 言語別LOC構成比

### 🎉 開発祭り演出
- **ヒーローセクション**: 総数を巨大カウンターで表示
- **リアルタイム更新**: 最新の活動状況を即座に反映
- **インタラクティブチャート**: リポジトリ別統計の可視化
- **美しいUI**: グラデーション背景とアニメーション効果

## セットアップ

### 必要な環境
- Python 3.8+
- pip

### インストール
```bash
# 依存関係をインストール
pip install -r requirements.txt

# 統計データを収集
python3 collect_stats.py

# Webダッシュボードを起動
python3 app.py
```

### GitHub API認証（オプション）
より多くのAPIリクエストを行うには、GitHub tokenを設定してください：

```bash
export GITHUB_TOKEN=your_github_token_here
```

## 使用方法

1. **データ収集**: `python3 collect_stats.py` で最新の統計情報を取得
2. **ダッシュボード起動**: `python3 app.py` でWebサーバーを開始
3. **ブラウザでアクセス**: http://localhost:5000 でダッシュボードを表示
4. **リアルタイム更新**: ダッシュボード上の「データ更新」ボタンで最新情報に更新

## ファイル構成

```
oss-statistics/
├── README.md              # このファイル
├── requirements.txt       # Python依存関係
├── collect_stats.py      # GitHub API統計収集スクリプト
├── app.py               # Flask Webアプリケーション
├── stats.json           # 収集された統計データ
├── templates/
│   └── dashboard.html   # ダッシュボードHTMLテンプレート
└── static/
    ├── css/
    │   └── style.css    # スタイルシート
    └── js/
        └── dashboard.js # JavaScript機能
```

## 今後の拡張予定

### 🚀 高度な統計機能
- **速度指標**: 平均PRレビュー時間、Issue→PRリードタイム
- **品質指標**: CI成功率、リオープンIssue率
- **コミュニケーション**: リアクション数、ワードクラウド

### 🎮 ゲーミフィケーション
- **リーダーボード**: 個人・リポジトリランキング
- **バッジシステム**: Newcomer、Streak、MVP等の自動付与
- **達成アラート**: 目標突破時の祝祭演出

### 📈 可視化強化
- **ヒートマップ**: リポジトリ×時間の活動状況
- **タイムライン**: PR→レビュー→マージの流れ
- **言語分析**: 言語別LOCの推移

## 技術スタック

- **バックエンド**: Python, Flask
- **フロントエンド**: HTML, CSS, JavaScript
- **チャート**: Chart.js
- **API**: GitHub REST API
- **データ**: JSON形式での永続化

## ライセンス

MIT License
