# 0thOpinion_Backend
ペットの予診アプリ。フロントエンドにNext.js、バックエンドにFlaskを使用。

# 起動前にやること
・backendフォルダ内に.envファイルを作成
  .envの中身
  シークレットキー
  SECRET_KEY=自由に設定（適当でいい）
  JWT_SECRET_KEY=自由に設定（適当でいい）
  
  OpenAI APIキー
  OPENAI_API_KEY=自分のAPIキー
  
  データベース接続情報
  DATABASE_USER=root
  DATABASE_PASSWORD=設定したパスワード
  DATABASE_HOST=localhost
  DATABASE_NAME=0thopiniondb

  
# 起動方法
・MySQLを使用しデータベースを作成
・データベースはMySQLをダウンロードしPCにインストールし、VScodeにMySQLの拡張機能（発行元：Weijan Chen）を入れ、create_0thOpinionDB.sqlを上から順に実行すれば作成可能
・ターミナルをバックエンドで開く 
・python -m venv venv 
・venv\Scripts\activate 
・pip install -r requirements.txt（初回だけ） 
・python run.py 
・これでバックエンド起動
