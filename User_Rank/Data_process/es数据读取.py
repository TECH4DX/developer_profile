from elasticsearch import Elasticsearch

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


query = es.search(index='gitee_issues',
                  body=query_json_all(),
                  scroll='5m',
                  size=2000)["hits"]["hits"]
issue_id = []
for i in query:
    print(i['_source']['id_in_repo'])
    issue_id.append(i['_source']['id_in_repo'])
print(issue_id)
