"""
Flaskをインポート
"""
from flask import Flask, request, jsonify
import uuid
import json

app = Flask(__name__)

rooms = {}

@app.route('/')
def index() -> str:
    """
    '/'にアクセスされたときの処理を行う関数
    """
    return 'hello world!'

@app.route('/room', methods=["POST", "GET"])
def join() -> dict:
    """
    しりとりのルームに関する状態を取得するAPI

    POSTならルームへの参加
    GETならルーム状態の取得
    """
    if (request.method == "POST"):
        data = json.loads(request.data.decode('utf-8'))
        print(data)
        print(rooms)
        roomids = list(rooms.keys())
        if (len(rooms.keys()) > 0 and len(rooms[roomids[-1]]['players']) == 1):
            rooms[roomids[-1]]['players'].append(data['id'])
            rooms[roomids[-1]]['status'] = 'playing'
            return {'roomId': roomids[-1]}
        else:
            roomid = str(uuid.uuid4())
            print(roomid)
            rooms[roomid] = {
                'players': [data['id']],
                'shiritori': ['しりとり'],
                'status': 'matching'
            }
            return {'roomId': roomid}
    elif (request.method == "GET"):
        params = request.args.to_dict()
        roomid = params['roomid']
        print(roomid, rooms[roomid]['players'])
        ready = len(rooms[roomid]['players']) == 2
        return {'ready': ready, 'member': rooms[roomid]['players']}
    else:
        return {'error': 'invalid request'}

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        load_dotenv=False
    )
