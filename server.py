from flask import Flask, request, abort
import requests
import json
import re

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
                            "ID": "1",
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
                    info['records'][0]['fields']['ID'] = ID
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
            print(response.text)
        elif res['event'] == 'ONTASKUPDATE':
            ID = res['data[FIELDS_AFTER][ID]']
            print(res)
            data = requests.get('https://viantec.bitrix24.ru/rest/345/7z6g7j7n1loz8nk5/task.item.list.json').json()
            full = requests.get(address, headers={"Authorization": fin})
            print(full.text)
            reg = r'{[\w\d" А-Яа-я,:\-\.]*{[\w\d" А-Яа-я,:\-\.]*"ID":' + f'"{ID}"'
            work = re.findall(reg, full.text)
            almost = re.findall(r'"id":".*?",', work[0])
            task_id = almost[0][6:-2]
            print(task_id)
            info = {
                "records": [
                    {
                        "id": task_id,
                        "fields": {
                            "Name": "Задача 4",
                            "ID": "1",
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
                    info['records'][0]['fields']['ID'] = ID
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
            response = requests.patch(address, headers=headers, json=info)
            print(response.text)
        elif res['event'] == 'ONTASKDELETE':
            ID = res['data[FIELDS_BEFORE][ID]']
            print(res)
            full = requests.get(address, headers={"Authorization": fin})
            print(full.text)
            reg = r'{[\w\d" А-Яа-я,:\-\.]*{[\w\d" А-Яа-я,:\-\.]*"ID":' + f'"{ID}"'
            work = re.findall(reg, full.text)
            almost = re.findall(r'"id":".*?",', work[0])
            task_id = almost[0][6:-2]
            print(task_id)
            params = {
                'records[]': [task_id]
            }

            response = requests.delete(address, headers=headers, params=params)
            print(response.status_code)
            print(response.json())
        
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
