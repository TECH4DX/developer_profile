import requests
import pandas as pd
import re
from elasticsearch import Elasticsearch

es = Elasticsearch(['34.96.160.229'], http_auth=('elastic', 'opensource'), port=9200, timeout=50000)

headers = {'User-Agent': 'Mozilla/5.0',
           # 'Authorization': 'token 42fb62b1c1ae8a57e75cc5d7a4abf90e91de9b58',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }


def query_json_all(field):  # 查询
    query_json = {
        "query": {
            "exists": {
                "field": field
            }
        }
    }
    return query_json


def issue_id():
    query = es.search(index='gitee_issues',
                      body=query_json_all('id_in_repo'),
                      scroll='5m',
                      size=2000)["hits"]["hits"]
    issue_id = []
    for i in query:
        print(i['_source']['id_in_repo'])
        issue_id.append(i['_source']['id_in_repo'])
    print(issue_id)
    return issue_id


def pr_id():
    query = es.search(index='gitee_prs',
                      body=query_json_all('id_in_repo'),
                      scroll='5m',
                      size=2000)["hits"]["hits"]
    pr_id = []
    for i in query:
        print(i['_source']['id_in_repo'])
        pr_id.append(i['_source']['id_in_repo'])
    print(pr_id)
    return pr_id


def crawel(es_id, crawel_type):
    # Issue
    # https://gitee.com/api/v5/repos/mindspore/issues/I4HELY/operate_logs?access_token=754436b59b9db45fd67615e444dc9bfb&repo=mindspore&sort=desc
    # PR
    # https://gitee.com/api/v5/repos/mindspore/mindspore/pulls/25550/operate_logs?access_token=754436b59b9db45fd67615e444dc9bfb&sort=desc
    index = 0
    event_id, event_type, login, repo, org, event_content, created_at, payload, pull_request, comment, repository = [], [], [], [], [], [], [], [], [], [], []
    for gitee_id in es_id:
        print('正在爬取第', gitee_id)
        if crawel_type == 'issue':
            url = 'https://gitee.com/api/v5/repos/mindspore/issues/' + gitee_id + '/operate_logs?access_token=754436b59b9db45fd67615e444dc9bfb&repo=mindspore&sort=desc'
        elif crawel_type == 'pr':
            url = 'https://gitee.com/api/v5/repos/mindspore/mindspore/pulls/' + gitee_id + '/operate_logs?access_token=754436b59b9db45fd67615e444dc9bfb&sort=desc'

        response = requests.get(url=url, headers=headers)
        data = response.json()
        if (response.status_code != 200):  # 檢測是否請求成功，若成功，狀態碼應該是200
            print('error: fail to request')
        for i in range(0, len(data)):
            event_data = data[i]
            event_id.append(event_data['id'])
            event_type.append(event_data['action_type'])
            login.append(event_data['user']['login'])
            event_content.append(event_data['content'])
            created_at.append(event_data['created_at'])

            # pull_request.append(event_data['payload']['pull_request'])
            # comment.append(event_data['payload']['comment'])
            # repository.append(event_data['payload'])
        if index % 10 == 0:
            mindspore_event_data = pd.DataFrame(
                {
                    'event_id': event_id,
                    'event_type': event_type,
                    'login': login,
                    'event_content': event_content,
                    'created_at': created_at,
                    # 'pull_request': pull_request,
                    # 'comment': comment,
                    # 'repository': repository,
                })
            file_name = 'mindspore_issue_' + crawel_type + '_data_1119.csv'
            mindspore_event_data.to_csv(file_name, index=None)
            print('已存储！')
        index += 1
    mindspore_event_data = pd.DataFrame(
        {
            'event_id': event_id,
            'event_type': event_type,
            'login': login,
            'event_content': event_content,
            'created_at': created_at,
            # 'pull_request': pull_request,
            # 'comment': comment,
            # 'repository': repository,
        })
    file_name = 'mindspore_issue_' + crawel_type + '_data_1119.csv'
    mindspore_event_data.to_csv(file_name, index=None)
    print('已存储！')


if __name__ == '__main__':
    # issue_id = issue_id()
    # crawel(es_id=issue_id, crawel_type='issue')
    prs_id = pr_id()
    crawel(es_id=prs_id, crawel_type='pr')
