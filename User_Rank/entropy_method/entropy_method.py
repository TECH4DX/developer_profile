import numpy as np
import pandas as pd


def calc_ent(x, x_value_list):
    """
        calculate shanno ent of x
    """
    event_name = []
    weight_val = []
    # unassigned,
    print(x_value_list)
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]  # 事件发生的概率
        logp = np.log2(p)  # log(p)
        ent -= p * logp
        event_name.append(x_value)
        weight_val.append(-p * logp)
    return ent, event_name, weight_val


def calc_ent_weight(ent, event_name, weight_val):
    index = 0
    print_event_name = []
    print_weight_val = []
    for val in weight_val:
        w = (1 - val) / (len(weight_val) - ent)
        print(event_name[index], w)
        print_event_name.append(event_name[index])
        print_weight_val.append(w)
        index += 1
    return print_event_name, print_weight_val


if __name__ == '__main__':
    event = pd.read_csv('../event_data/tensorflow_issue_event_0916_login.csv')['event']
    # 若Ｈ（ｘ）在第ｉ个动作维度上的熵值越大，则信息量越大，说明第ｉ个动作对于开发者的辨识度越低，也就意味着所有人更倾向于执行这个动作
    # x_value_list = set([x[i] for i in range(x.shape[0])]) # 全量
    x_value_list = ['labeled', 'subscribed', 'mentioned', 'assigned', 'unlabeled', 'closed', 'review_requested',
                    'moved_columns_in_project', 'unassigned', 'referenced', 'added_to_project', 'merged']
    ent, event_name, weight_val = calc_ent(event, x_value_list)
    print(ent)
    print_event_name, print_weight_val = calc_ent_weight(ent, event_name, weight_val)
    calc_ent = pd.DataFrame({
        'event_name': print_event_name,
        'weight_val': print_weight_val
    })
    calc_ent.to_csv('entropy_weight.csv', index=None)
