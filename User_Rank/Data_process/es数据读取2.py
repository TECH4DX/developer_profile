from elasticsearch import Elasticsearch
import pandas as pd

# es = Elasticsearch([{"host": "34.96.160.229", "port": 9200}])
es = Elasticsearch(['34.96.160.229'], http_auth=('elastic', 'opensource'), port=9200, timeout=50000)


def query_json_all():  # 查询
    query_json = {
        "query": {
            "exists": {
                "field": "id_in_repo"
            }
        }
    }
    return query_json


# query = es.search(index='gitee_issues',
#                   body=query_json_all(),
#                   scroll='5m',
#                   size=2000)["hits"]["hits"]
# issue_id = []
# for i in query:
#     print(i['_source']['id_in_repo'])
#     issue_id.append(i['_source']['id_in_repo'])
# print(issue_id)
issueList = es.search(index='issues_comment-enriched', scroll='1m', size=1000)
total = issueList["hits"]['total']
scroll_id = issueList['_scroll_id']
result = issueList['hits']['hits']
for i in range(0, int(total / 1000) + 1):
    result += es.scroll(scroll_id=scroll_id, scroll='1m')['hits']['hits']
count = 0
event_id, event_type, user_login, event_content, created_at = [], [], [], [], []
for i in result:
    if i['_source']['action'] == 'comment':
        event_id.append(count)
        event_type.append(i['_source']['action'])
        user_login.append(i['_source']['user_login_'])
        event_content.append(i['_source']['action'])
        created_at.append(i['_source']['update_at'])
    count += 1
comment_event = pd.DataFrame({
    'event_id': event_id,
    'event_type': event_type,
    'user_login': user_login,
    'event_content': event_content,
    'created_at': created_at
})
comment_event.to_csv('comment_event.csv', index=None)
