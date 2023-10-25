import uuid
import json
from flask import Flask, request

app = Flask(__name__)

rooms = {}

# consts
ROOM_KEY_PLAYERS = 'players'
ROOM_KEY_SHIRITORI = 'shiritori'
ROOM_KEY_STATUS = 'status'
STATUS_MATCHING = 'matching'
STATUS_PLAYING = 'playing'
STATUS_FINISHED = 'finished'

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
        # POSTのときの処理

        # POSTリクエストのbodyにあるデータを取り出してデコード
        # JSONとして解釈して辞書型的に使える形式にして data に代入
        data = json.loads(request.data.decode('utf-8'))
        # 今あるルームのIDのリストを取得
        roomids = list(rooms.keys())

        if (len(roomids) > 0\
                and rooms[roomids[-1]][ROOM_KEY_STATUS] == STATUS_MATCHING):
            # ルームが1以上あり、
            # かつ最後のルームのプレイヤーが一人なら

            # ルームに参加してステータスをプレイ中にする
            rooms[roomids[-1]][ROOM_KEY_PLAYERS].append(data['id'])
            rooms[roomids[-1]][ROOM_KEY_STATUS] = STATUS_PLAYING
            # 入ったルームを返す
            return {'roomId': roomids[-1]}
        
        else:
            # ルームが無い
            # もしくは最後のルームのプレイヤーが一人でないなら

            # ルームを新しく作成する
            roomid = str(uuid.uuid4())
            rooms[roomid] = {
                ROOM_KEY_PLAYERS: [data['id']],
                ROOM_KEY_SHIRITORI: ['しりとり'],
                ROOM_KEY_STATUS: STATUS_MATCHING
            }
            # 入ったルームを返す
            return {'roomId': roomid}

    elif (request.method == "GET"):
        # GETのときの処理

        # クエリパラメータからルームIDを取得
        params = request.args.to_dict()
        roomid = params['roomid']

        # ルームのステータスが 'playing' ならTrueに
        # そうでないならFalseになる
        ready = rooms[roomid][ROOM_KEY_STATUS] == STATUS_PLAYING
        # ルームの準備状況とメンバーを返す
        return {'ready': ready, 'member': rooms[roomid][ROOM_KEY_PLAYERS]}

@app.route('/shiritori/<roomid>', methods=["POST", "GET"])
def shiritori(roomid) -> dict:
    """
    しりとりをやり取りするAPI

    pathparamからルームIDを取得する

    POSTならしりとりに回答する
    GETなら現在の最後の回答を取得する
    """
    if (request.method == "POST"):
        # POSTのときの処理

        # POSTリクエストのbodyにあるデータを取り出してデコード
        # JSONとして解釈して辞書型的に使える形式にして data に代入
        data = json.loads(request.data.decode('utf-8'))
        # dataから回答を抜き出す
        answer = data['answer']

        # ルーム情報からしりとりの履歴を取得
        shiritories = rooms[roomid][ROOM_KEY_SHIRITORI]
        lastword = shiritories[-1]

        # 最後のことばの最後の文字と回答の最初の文字が等しいかどうか
        is_same_last_letter_and_firtst_lettar = lastword[-1] == answer[0]
        # 回答の最後の文字が ん であるかどうか
        is_last_letter_NN = answer[-1] == 'ん'
        # 回答が既に使われたことばかどうか
        is_appeared = answer in shiritories

        # ルームの履歴に回答を追加する
        rooms[roomid][ROOM_KEY_SHIRITORI].append(answer)

        if (not is_same_last_letter_and_firtst_lettar\
                or is_last_letter_NN\
                or is_appeared):
            # しりとりのルールを守れていない回答なら

            # ルームのステータスを 'finished' にする
            rooms[roomid][ROOM_KEY_STATUS] = STATUS_FINISHED
            # 敗北したことを返す
            return {'result': 'defeat'}

        else:
            # しりとりのルールが守られている回答なら

            # 回答が成功したことを返す
            return {'result': 'collect'}

    elif (request.method == "GET"):
        # GETのときの処理

        # ルームのしりとり履歴を取得
        shiritories = rooms[roomid][ROOM_KEY_SHIRITORI]

        if (rooms[roomid][ROOM_KEY_STATUS] == STATUS_FINISHED):
            # ルームのステータスが 'finished' なら

            # 勝利したことを返す
            return {'result': 'victory'}

        elif ((rooms[roomid][ROOM_KEY_STATUS] == STATUS_PLAYING)):
            # ルームのステータスがプレイ中なら

            # 現在の最後の回答を返す
            return {
                'lastword': shiritories[-1],
                'words': len(shiritories)
            }

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        load_dotenv=False
    )
