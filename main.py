"""
- 現在日時の取得のためにdatetimeをインポート
- flaskから必要なパッケージをインポート
- Flask
- render_template
"""
import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> str:
    """
    '/'にアクセスされたときの処理を行う関数
    """
    nowstr = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    return render_template('index.html.j2', current_time=nowstr)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        load_dotenv=False
    )
