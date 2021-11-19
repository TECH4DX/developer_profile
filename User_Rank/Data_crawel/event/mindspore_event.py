import requests
import pandas as pd
import re

headers = {'User-Agent': 'Mozilla/5.0',
           # 'Authorization': 'token 42fb62b1c1ae8a57e75cc5d7a4abf90e91de9b58',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }
# https://gitee.com/api/v5/repos/mindspore/mindspore/events?access_token=daaaa59324acf294b623a74305369255&limit=100
index = 0
event_id, event_type, login, repo, org, created_at, payload, pull_request, comment, repository = [], [], [], [], [], [], [], [], [], []
for i in range(0, 100):
    print('正在爬取第', i, '页')
    url = 'https://gitee.com/api/v5/repos/mindspore/mindspore/events?access_token=daaaa59324acf294b623a74305369255&limit=100' + '&page=' + str(
        i)
    response = requests.get(url=url, headers=headers)
    data = response.json()
    if (response.status_code != 200):  # 檢測是否請求成功，若成功，狀態碼應該是200
        print('error: fail to request')
    for i in range(0, len(data)):
        event_data = data[i]
        if event_data['actor']['login'] == 'I-am-a-robot':
            continue
        event_id.append(event_data['id'])
        if event_data['type'] == 'IssueEvent':
            event_type.append(event_data['payload']['action'])
        else:
            event_type.append(event_data['type'])
        login.append(event_data['actor']['login'])
        repo.append(event_data['repo']['full_name'])
        org.append(event_data['org']['login'])
        created_at.append(event_data['created_at'])
        payload.append(event_data['payload'])
        # pull_request.append(event_data['payload']['pull_request'])
        # comment.append(event_data['payload']['comment'])
        # repository.append(event_data['payload'])
    if index % 10 == 0:
        mindspore_event_data = pd.DataFrame(
            {
                'event_id': event_id,
                'event_type': event_type,
                'login': login,
                'repo': repo,
                'org': org,
                'created_at': created_at,
                # 'pull_request': pull_request,
                # 'comment': comment,
                # 'repository': repository,
            })
        mindspore_event_data.to_csv('mindspore_event_data_1118_10000.csv', index=None)
        print('已存储！')
    index += 1
mindspore_event_data = pd.DataFrame(
    {
        'event_id': event_id,
        'event_type': event_type,
        'login': login,
        'repo': repo,
        'org': org,
        'created_at': created_at,
        # 'pull_request': pull_request,
        # 'comment': comment,
        # 'repository': repository,
    })
mindspore_event_data.to_csv('mindspore_event_data_1118_10000.csv', index=None)
print('已存储！')
