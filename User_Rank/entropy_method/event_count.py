import pandas as pd


def get_index(list=None, item=''):
    return [index for (index, value) in enumerate(list) if value == item]


def user_event_score(user_list, event_data):
    event_labled, event_assigned, event_referenced, event_mentioned, event_review_requested, event_ready_for_review = [], [], [], [], [], []
    event_closed = []
    event_event_assignee, event_event_assigner, event_review_requester, event_requested_reviewer = [], [], [], []
    for user_id in user_list:
        print(user_id)
        index_event_c1 = get_index(list(event_data['actor']), user_id)
        event_labeled_s, event_assigned_s, event_referenced_s = 0, 0, 0
        event_mentioned_s, event_review_requested_s, event_ready_for_review_s = 0, 0, 0
        event_closed_s = 0
        for i in index_event_c1:
            if event_data['event'][i] == 'labeled':  # 打标签
                event_labeled_s += 1
            elif event_data['event'][i] == 'referenced':  # ?
                event_referenced_s += 1
            elif event_data['event'][i] == 'mentioned':  # 被@
                event_mentioned_s += 1
            elif event_data['event'][i] == 'review_requested':  #
                event_review_requested_s += 1
            elif event_data['event'][i] == 'ready_for_review':  # review问题者
                event_ready_for_review_s += 1
            elif event_data['event'][i] == 'closed':  # 关闭问题者
                event_closed_s += 1

        index_event_assignee = get_index(list(event_data['assignee']), user_id)
        event_assignee_s = len(index_event_assignee)

        index_event_assigner = get_index(list(event_data['assigner']), user_id)
        event_assigner_s = len(index_event_assigner)

        # index_event_review_requester = get_index(list(issue_event['review_requester']), user_id)
        # event_review_requester_s = len(index_event_review_requester)
        #
        # index_event_requested_reviewer = get_index(list(issue_event['requested_reviewer']), user_id)
        # event_requested_reviewer_s = len(index_event_requested_reviewer)

        event_labled.append(event_labeled_s)
        # event_assigned.append(event_assigned_s)
        event_referenced.append(event_referenced_s)
        event_mentioned.append(event_mentioned_s)
        event_closed.append(event_closed_s)

        event_review_requested.append(event_review_requested_s)
        event_ready_for_review.append(event_ready_for_review_s)

        event_event_assignee.append(event_assignee_s)
        event_event_assigner.append(event_assigner_s)
        # event_review_requester.append(event_review_requester_s)
        # event_requested_reviewer.append(event_requested_reviewer_s)

    event_active = pd.DataFrame({
        'user_list': user_list,

        'labeled': event_labled,
        'event_referenced': event_referenced,
        'event_mentioned': event_mentioned,
        'event_closed': event_closed,

        'event_event_assignee': event_event_assignee,
        'event_event_assigner': event_event_assigner,
        'event_review_requester': event_review_requested,
        'event_requested_reviewer': event_ready_for_review
    })
    # event_labled, event_referenced, event_mentioned, event_closed, \
    #            event_event_assignee, event_event_assigner, \
    #            event_review_requested, event_ready_for_review
    return event_active
