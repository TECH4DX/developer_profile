import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

versioinID = 0.10

search_index = 'gitee_issues-raw'
index_name = 'issue_data-analyzer'

user_name = ''
passwd = ''
es_host = '127.0.0.1'
es_port = 9200
gitee_token = 'xxxx'

'''
Notice: 
The implementation of function 'is_promoted' was from
https://gitee.com/mindspore/community/blob/master/sigs/dx/issue_analysis/scripts/event_classifier.py,
which was done by BoxuanZhao before.
'''
# 遍历issue列表时调用，以判断该条issue是否满足三个条件
def is_promoted(owner_id, issue_operate_logs, issue_comments):
    # 这里某些项以后可以设置成integer，用以表示单条issue里正面行为的次数（比如打了多个标签）
    total_flag = False
    label_flag = False
    assign_flag = False
    other_flag = False

    # 先看日志里是否有推进issue解决的正面行为
    for action in issue_operate_logs:
        action_owner_id = action['user']['id']
        action_icon = action['icon']
        # 有没有打标签
        if action_owner_id == owner_id and action_icon == 'tag icon':
            label_flag = True
        # 有没有指派负责人/协作人
        if action_owner_id == owner_id and action_icon == 'add user icon':
            assign_flag = True
        # 有没有其他推进issue解决的行为（如设置schedule/milestone）
        if action_owner_id == owner_id and (action_icon != 'add user icon' and action_icon != 'tag icon'):
            other_flag = True

    # 再看评论区里是否有推进issue解决的正面行为
    def is_label_comment(issue_comment):
        # 先简单判断一下前两个字符是不是均为/
        if issue_comment['body'][0] == '/' and issue_comment['body'][1] == '/':
            return True
        else:
            return False

    for comment in issue_comments:
        comment_owner_id = comment['user']['id']
        # 有没有通过评论打标签
        if comment_owner_id == owner_id and is_label_comment(comment):
            label_flag = True
        # 有没有在自己的issue下做回复（不包括与bot互动）
        if comment_owner_id == owner_id and comment['body'][0] != '/':
            other_flag = True

    total_flag = label_flag or assign_flag or other_flag

    return total_flag, label_flag, assign_flag, other_flag

if __name__ == '__main__' :
    print("Version: ", versioinID)
    
    es = Elasticsearch([{"host": es_host, "port": es_port}], http_auth=(user_name, passwd))
    if es.ping():
        print("es info:")
        print(es.info())
    else:
        print("es not connected")
        exit()

    issueList = es.search(index=search_index, scroll='1m', size=1000)

    total = issueList["hits"]['total']
    print("find {0} issues".format(total))

    scroll_id = issueList['_scroll_id']

    issues = issueList['hits']['hits']
    for i in range(0, int(total/1000) + 1):
        issues += es.scroll(scroll_id=scroll_id, scroll='1m')['hits']['hits']

    actions = []
    for issue in issues:
        issue_data = issue['_source']['data']
        created_at = issue_data['created_at']
        issue_id = issue_data['id']
        number = issue_data['number']  # Gitee issue URL
        owner = issue_data['user']
        owner_id = owner['id']
        owner_login = owner['login']
        owner_name = owner['name']

        repo = issue_data['repository']['name']

        issue_operate_logs = requests.get(
            f"https://gitee.com/api/v5/repos/{repo}/issues/{number}/operate_logs",
            params={'access_token': gitee_token, 'repo': repo, 'sort': 'desc'}).json()

        total_flag, label_flag, assign_flag, other_flag = is_promoted(owner_id, issue_operate_logs, issue_data['comments_data'])

        body = {
                'id': issue_id,
                'number': number,
                'owner_id': owner_id,
                'owner_login': owner_login,
                'owner_name': owner_name,
                'total_flag': total_flag,
                'label_flag': label_flag,
                'assign_flag': assign_flag,
                'other_flag': other_flag,
                'created_at': created_at
                }

        id = hash(str(issue_id) + created_at)

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

    print("Job done! \n")
