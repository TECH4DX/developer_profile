import pandas as pd
import numpy as np
from User_Rank.entropy_method.entropy_method import calc_ent, calc_ent_weight
from User_Rank.entropy_method.event_count import user_event_score
from elasticsearch import Elasticsearch

es = Elasticsearch(['34.96.160.229'], http_auth=('elastic', 'opensource'), port=9200, timeout=50000)


def get_index(list=None, item=''):
    return [index for (index, value) in enumerate(list) if value == item]


def calculate_score(event_data, used_event_list, entropy_weight):
    event_user = np.unique(list(event_data['user_login']))
    user_score_list, user_name = [], []
    for name in event_user:
        user_score = 0
        event_index = get_index(event_data['user_login'], name)
        for index in event_index:
            if event_data['event_type'][index] in used_event_list:
                user_score += print_weight_val[get_index(used_event_list, event_data['event_type'][index])[0]]
        user_name.append(name)
        user_score_list.append(user_score)
    user_score_rank = pd.DataFrame({
        'user_login': user_name,
        'user_score': user_score_list})
    # user_score_rank.to_csv('user_score_rank.csv', index=None)
    print(user_score_rank)
    return user_score_rank


def comment_data():
    # issueList = es.search(index='issues_comment-enriched', scroll='1m', size=1000)
    # total = issueList["hits"]['total']
    # scroll_id = issueList['_scroll_id']
    # result = issueList['hits']['hits']
    # for i in range(0, int(total / 1000) + 1):
    #     result += es.scroll(scroll_id=scroll_id, scroll='1m')['hits']['hits']
    # count = 0
    # event_id, event_type, user_login, event_content, created_at = [], [], [], [], []
    # for i in result:
    #     if i['_source']['action'] == 'comment':
    #         event_id.append(count)
    #         event_type.append(i['_source']['action'])
    #         user_login.append(i['_source']['user_login_'])
    #         event_content.append(i['_source']['action'])
    #         created_at.append(i['_source']['update_at'])
    #     count += 1
    # comment_event = pd.DataFrame({
    #     'event_id': event_id,
    #     'event_type': event_type,
    #     'user_login': user_login,
    #     'event_content': event_content,
    #     'created_at': created_at
    # })
    # comment_event.to_csv('comment_event.csv', index=None)

    comment_event = pd.read_csv('Data_process/comment_event.csv')
    return comment_event


def calculated_rank(event_active):
    event_list = list(event_active.columns[1:])
    user_name_list = event_active['user_login']
    user_id_list = []
    user_id = 0
    for columns in event_list:
        data = event_active.sort_values(by=columns, ascending=False)
        temp_list = []
        print(data['user_login'])
        for name in user_name_list:
            index = get_index(list(data['user_login']), name)
            temp_list.append(index[0] + 1)

        event_active[columns] = temp_list
    print(event_active)
    event_active.to_csv('user_event_rank2.csv')
    # print(data['user_login'])
    # print(data[columns])


if __name__ == '__main__':
    event_data = pd.read_csv('Data_crawel/event_v2/mindspore_issue_issue_data_1122.csv')  # Issue
    print(event_data)
    comment_event = comment_data()

    # comment event 数据合并
    event_data = pd.concat([event_data, comment_event], axis=0)
    # event_data.to_csv('event_data.csv', index=None)
    event_data = event_data.reset_index(drop=True)
    print(event_data)

    # 数据清理 去除机器人操作
    index = []
    count = 0
    for name in event_data['user_login']:
        if name == 'I-am-a-robot' or name == 'mindspore_ci' or name == 'test-bot':
            index.append(count)
        if str(event_data['event_type'][count]) == 'change_issue_state':
            if '修改为DONE' not in str(event_data['event_content'][count]):
                # print(str(event_data['event_content'][count]))
                index.append(count)
        if type(event_data['event_type'][count]) != str:
            index.append(count)
        count += 1
    event_data.drop(index, inplace=True)
    event_data = event_data.reset_index(drop=True)
    # print(event_data)

    # 评估event的权重
    event = event_data['event_type']
    for i in event:
        if type(i) != str:
            print(i)
    print(np.unique(event))
    print(pd.value_counts(event))

    # used_event_list = list(np.unique(event))
    used_event_list = ['create', 'assign_collaborator', 'setting_assignee', 'change_issue_state', 'comment']
    print(list(used_event_list))
    ent, event_name, weight_val = calc_ent(event, used_event_list)
    print_event_name, print_weight_val = calc_ent_weight(ent, event_name, weight_val)
    entropy_weight = pd.DataFrame({
        'event_name': print_event_name,
        'weight_val': print_weight_val
    })
    entropy_weight.to_csv('entropy_weight.csv', index=None)

    # 统计用户event次数
    event_user = np.unique(list(event_data['user_login']))
    event_active = user_event_score(user_list=event_user, event_data=event_data)
    event_active.to_csv('Issue_event_count.csv', index=None)

    # calculate score
    user_score_rank = calculate_score(event_data, used_event_list, entropy_weight)
    event_active['Score'] = user_score_rank['user_score']
    event_active.to_csv('user_event_score.csv', index=None)

    # calculated rank
    calculated_rank(event_active)
