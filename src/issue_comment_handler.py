from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

versioinID = 0.10

search_index = 'gitee_issues-raw'
index_name = 'issues_comment-enriched'

user_name = ''
passwd = ''
es_host = '127.0.0.1'
es_port = 9200

if __name__ == '__main__' :
    print("Version: ", versioinID)
    
    es = Elasticsearch([{"host": es_host, "port": es_port}], http_auth=(user_name, passwd))
    if es.ping():
        print("es info:")
        print(es.info())
    else:
        print("es not connected")
        exit()

    # body = {
    #     "user_name": "test-bot",
    #     "user_login": "test-bot-s",
    #     "id": "0001"
    # }

    # insert document
    # es.index(index="test-data", doc_type='_doc', document=body)

    issueList = es.search(index=search_index, scroll='1m', size=1000)

    total = issueList["hits"]['total']
    print("find {0} issues".format(total))

    scroll_id = issueList['_scroll_id']

    result = issueList['hits']['hits']
    for i in range(0, int(total/1000) + 1):
        result += es.scroll(scroll_id=scroll_id, scroll='1m')['hits']['hits']

    actions = []
    for hit in result:
        source = hit['_source']
        data = source['data']

        for event in ['creater', 'assignee', 'collaborators', 'comments']:
        
            if event == 'creater':
                tasks = ['creater']
            elif event == 'assignee':
                if data['assignee'] == None:
                    continue
                tasks = ['assignee']
            elif event == 'collaborators':
                tasks = ['collaborator'] * len(data['collaborators'])
            else:
                tasks = ['comment'] * len(data['comments_data'])

            for index, task in enumerate(tasks):
                
                action = task

                if task == 'creater':
                    user_login = data['user']['login']
                    update_at = data['created_at']

                elif task == 'assignee':
                    user_login = data['assignee_data']['login']
                    update_at = data['assignee_data']['created_at']

                elif task == 'collaborator':
                    user_login = data['collaborators_data'][index]['login']
                    update_at = data['collaborators_data'][index]['created_at']
                
                elif task == 'comment':
                    user_login = data['comments_data'][index]['user']['login']
                    update_at = data['comments_data'][index]['created_at']
                else:
                    print("not supported task!!")
                    exit(1)    

                body = {
                    'issue_id': data['id'],
                    'issue_number': data['number'],
                    'issue_state': data['state'],
                    'issue_type': data['issue_type'],
                    'issue_labels': data['labels'],
                    'repository': data['html_url'],
                    'creater_login': data['user']['login'],
                    'user_login': data['user']['login'],
                    'user_login_': user_login,
                    'action': action,
                    'update_at': update_at
                }

                id = hash(str(data['id']) + user_login + action + update_at)

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

    print("job done!")