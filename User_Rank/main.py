import pandas as pd
import numpy as np
from User_Rank.entropy_method.entropy_method import calc_ent, calc_ent_weight
from User_Rank.entropy_method.event_count import user_event_score


def get_index(list=None, item=''):
    return [index for (index, value) in enumerate(list) if value == item]


def calculate_score(event_data, used_event_list, entropy_weight):
    event_user = np.unique(list(event_data['login']))
    user_score_list, user_name = [], []
    for name in event_user:
        user_score = 0
        event_index = get_index(event_data['login'], name)
        for index in event_index:
            if event_data['event_type'][index] in used_event_list:
                user_score += print_weight_val[get_index(used_event_list, event_data['event_type'][index])[0]]
        user_name.append(name)
        user_score_list.append(user_score)
    user_score_rank = pd.DataFrame({
        'login': user_name,
        'user_score': user_score_list})
    user_score_rank.to_csv('user_score_rank.csv', index=None)
    print(user_score_rank)


if __name__ == '__main__':
    # event_data = pd.read_csv('Data_crawel/event_v2/mindspore_issue_event_data_1119.csv')  # Issue
    event_data = pd.read_csv('Data_crawel/event_v2/mindspore_pr_event_data_1119.csv')  # Issue

    # 数据清理 去除机器人操作
    index = []
    count = 0
    for name in event_data['login']:
        if name == 'I-am-a-robot' or name == 'mindspore_ci':
            index.append(count)
        if type(event_data['event_type'][count]) != str:
            index.append(count)
        count += 1
    event_data.drop(index, inplace=True)
    event_data = event_data.reset_index(drop=True)
    print(event_data)

    # 评估event的权重
    event = event_data['event_type']
    for i in event:
        if type(i) != str:
            print(i)

    print(event)
    print(np.unique(event))
    print(pd.value_counts(event))

    # used_event_list = ['labeled', 'subscribed', 'mentioned', 'assigned', 'unlabeled', 'closed', 'review_requested',
    #                    'moved_columns_in_project', 'unassigned', 'merged', 'referenced', 'added_to_project', 'merged']
    # used_event_list = list(np.unique(event)[0:10])
    used_event_list = list(np.unique(event))
    print(list(used_event_list))
    ent, event_name, weight_val = calc_ent(event, used_event_list)
    print_event_name, print_weight_val = calc_ent_weight(ent, event_name, weight_val)
    entropy_weight = pd.DataFrame({
        'event_name': print_event_name,
        'weight_val': print_weight_val
    })
    entropy_weight.to_csv('entropy_weight.csv', index=None)

    # # 统计用户event次数
    # event_user = np.unique(list(event_data['login']))
    # event_active = user_event_score(user_list=event_user, event_data=event_data)
    # event_active.to_csv('event_count.csv', index=None)
    # print(event_active)

    # calculate score
    calculate_score(event_data, used_event_list, entropy_weight)
