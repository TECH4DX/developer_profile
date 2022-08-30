import requests
import json
import datetime
from opensearchpy import OpenSearch, helpers
# from elasticsearch.helpers import bulk

host = '119.8.62.92'
port = 8200
auth = ('DX2022', 'opensource')

index_name = 'gitee_issues-raw'

gitee_token = '938ff3e3c19d6a9b8e8c878720c779eb'

#

def isCommentByBot(comment):
    if comment['user']['login'] == "I-am-a-robot":
        return True
    else:
        return False

def isInOrg(userLogin, orgName, accessToken):
    orgInfo = requests.get(
            "https://gitee.com/api/v5/users/{user_login}/orgs".format(user_login=userLogin),
            params={'access_token': accessToken, 'sort': 'desc'}).json()
    
    if len(orgInfo) == 0:
        return False
    for info in orgInfo:
        print("user_login: {}, org_name: {}".format(userLogin ,info['name']))
        if info['name'] == orgName:
            return True
    return False

if __name__ == '__main__' :

    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = False, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        timeout=30, 
        max_retries=10, 
        retry_on_timeout=True
        )

    connect = client.ping()
    print("Connect to DB: ", connect)

    query = {
        "query": {
            "multi_match": {
                "query": "mindspore",
                "fields": ["search_fields.owner"]
                }
            }
        }

    issueList = helpers.scan(
          client = client,
          index = index_name,
          query = query,
          size= 10
        )

    outUserList = {}

    countTotal = 0
    countInInterval = 0
    for issue in issueList:
        countTotal += 1
        issue_data = issue['_source']['data']
        created_at = issue_data['created_at']
        issue_id = issue_data['id']
        number = issue_data['number']  # Gitee issue URL
        owner = issue_data['user']
        owner_id = owner['id']
        owner_login = owner['login']
        owner_name = owner['name']
        comments = issue_data['comments_data']

        org = issue_data['repository']['namespace']['path']
        repo = issue_data['repository']['name']
        
        startTime = datetime.datetime.strptime("2022-01-01T00:00:00+08:00", r"%Y-%m-%dT%H:%M:%S+08:00")
        endTime = datetime.datetime.strptime("2022-06-30T23:59:59+08:00", r"%Y-%m-%dT%H:%M:%S+08:00")
        createdTime = datetime.datetime.strptime(created_at, r"%Y-%m-%dT%H:%M:%S+08:00")

        if startTime < createdTime < endTime and org == 'mindspore':
            countInInterval += 1
            for comment in comments:
                if isCommentByBot(comment):
                    outUserList[owner_login] = owner_name  
    
    with open("./data/users.json", "w") as fw:
            json.dump(outUserList, fw)
        
    print("countTotal: ", countTotal)
    print("countInInterval: ", countInInterval)
    print("outside users numbers: ", len(outUserList.keys()))
    print("Job done! \n")
