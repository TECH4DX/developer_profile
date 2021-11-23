# csv数据导入
import csv
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch(['34.96.160.229'], http_auth=('elastic', 'opensource'), port=9200, timeout=50000)


def create_index(index_name='gitee_event', index_type='en'):
    es = Elasticsearch(['34.96.160.229'], http_auth=('elastic', 'opensource'), port=9200, timeout=50000)

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
    index_name = 'gitee_issues_user_rank'
    # csv_reader = json.load('event_data/tensorflow_issue_event_0916_login.json')
    # csv_reader = csv.reader(open('../Data_crawel/event_v2/mindspore_issue_issue_data_1122.csv', 'r', encoding='UTF-8'))
    csv_reader = csv.reader(open('../user_event_rank2.csv', 'r', encoding='UTF-8'))

    # csv_reader = csv.reader(open('event_data/user_info.csv', 'r', encoding='UTF-8'))
    rows = [row for row in csv_reader]
    # print(rows[1:])
    if es.ping():
        print("es info:")
        print(es.info())
    else:
        print("es not connected")
        exit()

    actions = []
    for row in rows[1:]:
        body = {
            'user_login': row[1],
            'create_issue_rank': row[2],
            'comment_issue_rank': row[3],
            'assign_collaborator_rank': row[4],
            'setting_assignee_rank': row[5],
            'closed_issue_rank': row[6],
            'Overall_issue_rank': row[7]
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
