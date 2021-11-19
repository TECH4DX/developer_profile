# csv数据导入
import csv
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es_host = '34.96.160.229'
es_port = 9200


def create_index(index_name='gitee_event', index_type='en'):
    es = Elasticsearch([es_host])
    print(es.indices)
    '''
    创建索引,创建索引名称为ott，类型为ott_type的索引
    :param ex: Elasticsearch对象
    :return:
    '''
    # 创建映射
    # _index_mappings = {
    #     "mappings": {
    #         index_type: {
    #             "properties": {
    #                 "full_name": {
    #                     'type': 'text'
    #                 },
    #                 "name": {
    #                     'type': 'text'
    #                 },
    #                 "forks_count": {
    #                     'type': 'int'
    #                 },
    #                 "stargazers_count": {
    #                     'type': 'int'
    #                 },
    #                 "watchers_count": {
    #                     'type': 'int'
    #                 },
    #                 "open_issues_count": {
    #                     'type': 'int'
    #                 }
    #             }
    #         }
    #
    #     }
    # }
    # if es.indices.exists(index=index_name) is not True:
    #     res = es.indices.create(index=index_name, body=_index_mappings, ignore=400)
    #     print(res)


def gitee_event():
    index_name = 'gitee_event'
    # csv_reader = json.load('event_data/tensorflow_issue_event_0916_login.json')
    csv_reader = csv.reader(open('../event_data/tensorflow_issue_event_0916_login.csv', 'r', encoding='UTF-8'))
    # csv_reader = csv.reader(open('event_data/user_info.csv', 'r', encoding='UTF-8'))
    rows = [row for row in csv_reader]
    print(rows[1:])
    es = Elasticsearch([{"host": es_host, "port": es_port}])
    if es.ping():
        print("es info:")
        print(es.info())
    else:
        print("es not connected")
        exit()

    actions = []
    for row in rows[1:]:
        body = {
            'issue_id': row[0],
            'event_url': row[1],
            'id': row[2],
            'url': row[3],
            'actor': row[4],
            'commit_id': row[5],
            'commit_url': row[6],
            'event': row[7],
            'created_at': row[8],
            'rename': row[9],
            'label': row[10],
            'assignee': row[11],
            'assigner': row[12],
            'review_requester': row[13],
            'requested_reviewer': row[14]
        }

        id = row[0]
        index_action = {
            '_op_type': 'index',
            '_index': index_name,
            '_type': 'items',
            '_id': id,
            '_source': body
        }
        actions.append(index_action)
    print(actions)
    if actions:
        bulk(es, actions)


if __name__ == "__main__":
    # create_index()
    gitee_event()
