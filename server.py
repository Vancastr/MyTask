from flask import Flask, request, abort
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_out():
    if request.method == 'POST':
        address = "https://api.airtable.com/v0/app6lyEHjT1Da9eqD/Tasks/"
        api_key = "patX0YZPRODK1eZQT.6bb66da4cf03361055f032e8e64a6a01001888d2e25b5b775a37204885ae99a1"
        fin = "Bearer " + api_key
        headers = {
            "Authorization": fin,
            "Content-Type": "application/json"
        }
        res = request.form.to_dict()
        if res['event'] == 'ONTASKADD':
            ID = res['data[FIELDS_AFTER][ID]']
            print(res)
            data = requests.get('https://viantec.bitrix24.ru/rest/345/7z6g7j7n1loz8nk5/task.item.list.json').json()
            info = {
                "records": [
                    {
                        "fields": {
                            "Name": "Задача 4",
                            "Status": "In progress",
                            "Start date": "2023-12-13",
                            "Deadline": "2023-12-30"
                        }
                    }
                ]
            }
            for i in data['result']:
                if i['ID'] == ID:
                    info['records'][0]['fields']['Name'] = i['TITLE']
                    info['records'][0]['fields']['Deadline'] = i['DEADLINE'][:10]
                    info['records'][0]['fields']['Start date'] = i['CREATED_DATE'][:10]
                    if i['REAL_STATUS'] == '1':
                        info['records'][0]['fields']['Status'] = 'New'
                    elif i['REAL_STATUS'] == '2':
                        info['records'][0]['fields']['Status'] = 'To do'
                    elif i['REAL_STATUS'] == '3':
                        info['records'][0]['fields']['Status'] = 'In progress'
                    elif i['REAL_STATUS'] == '4':
                        info['records'][0]['fields']['Status'] = 'Waiting for approval'
                    elif i['REAL_STATUS'] == '5':
                        info['records'][0]['fields']['Status'] = 'Done'
            print(info)
            response = requests.post(address, headers=headers, json=info)
            resp = response.json()
            task_id = resp['records'][0]['id']
            with open('IDs.txt', 'r', encoding='utf-8') as file:
                js = json.load(file)
            js[0][ID] = task_id
            with open('IDs.txt', 'w', encoding='utf-8') as file:
                json.dump(js, file)
            print(response.text)
        elif res['event'] == 'ONTASKUPDATE':
            ID = res['data[FIELDS_AFTER][ID]']
        elif res['event'] == 'ONTASKDELETE':
            ID = res['data[FIELDS_BEFORE][ID]']
        print(res)
        data = requests.get('https://viantec.bitrix24.ru/rest/345/7z6g7j7n1loz8nk5/task.item.list.json').json()
        info = {
                "records": [
                    {
                        "fields": {
                            "Name": "Задача 4",
                            "Status": "In progress",
                            "Start date": "2023-12-13",
                            "Deadline": "2023-12-30"
                        }
                    }
                ]
            }
        
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
