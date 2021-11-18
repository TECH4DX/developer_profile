import csv
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

index_name = 'user_info'
user_name = ''
passwd = ''
es_host = '127.0.0.1'
es_port = 9200

if __name__ == "__main__":
    csv_reader = csv.reader(open('../data/user_info.csv', 'r', encoding='UTF-8'))
    rows = [row for row in csv_reader]
    
    es = Elasticsearch([{"host": es_host, "port": es_port}],http_auth=(user_name, passwd))
    if es.ping():
        print("es info:")
        print(es.info())
    else:
        print("es not connected")
        exit()
    
    now_time = time.strftime('%Y-%m-%dT%H:%M:%S%z',time.localtime())

    actions = []
    for row in rows[1:]:
        body = {
                'user_name': row[0],
                'user_login': row[1],
                'avatar_url': row[2],
                'followers_count': int(row[3]),
                'following_count': int(row[4]),
                'stared_count': int(row[5]),
                'watched_count': int(row[6]),
                'created_at': row[7],
                'updated_at': row[8],
                'enriched_at': now_time,
                'user_email': row[9],
                'user_bio': row[10]
            }

        id = row[1]

        index_action = {
            '_op_type': 'index',
            '_index': index_name,
            '_type': 'items',
            '_id': id,
            '_source': body
        }

        actions.append(index_action)

    if actions:
        bulk(es, actions)