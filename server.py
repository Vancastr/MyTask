from flask import Flask, request, abort
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_out():
    if request.method == 'POST':
        res = request.form.to_dict()
        ID = res['data[FIELDS_BEFORE][ID]']
        print(res)
        data = requests.get('https://viantec.bitrix24.ru/rest/345/7z6g7j7n1loz8nk5/task.item.list.json').json()
        info = {}
        for i in data['result']:
            if i['ID'] == ID:
                info['TITLE'] = i['TITLE']
                info['DEADLINE'] = i['DEADLINE']
                info['CREATED_DATE'] = i['CREATED_DATE']
                info['STATUS'] = i['STATUS']
        print(info)
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run()