import pandas as pd


def get_index(list=None, item=''):
    return [index for (index, value) in enumerate(list) if value == item]


def user_event_score(user_list, event_data):
    event_create, event_assign_collaborator, event_setting_assignee, event_change_issue_state, event_comment = [], [], [], [], []
    event_closed = []
    for user_id in user_list:
        print(user_id)
        index_event_c1 = get_index(list(event_data['user_login']), user_id)
        event_create_c, event_assign_collaborator_c, event_setting_assignee_c, event_change_issue_state_c, event_comment_c = 0, 0, 0, 0, 0
        for i in index_event_c1:
            if event_data['event_type'][i] == 'create':  # 打标签
                event_create_c += 1
            elif event_data['event_type'][i] == 'assign_collaborator':  # ?
                event_assign_collaborator_c += 1
            elif event_data['event_type'][i] == 'setting_assignee':  # 被@
                event_setting_assignee_c += 1
            elif event_data['event_type'][i] == 'change_issue_state':  #
                event_change_issue_state_c += 1
            elif event_data['event_type'][i] == 'comment':  #
                event_comment_c += 1
        # index_event_review_requester = get_index(list(issue_event['review_requester']), user_id)
        # event_review_requester_s = len(index_event_review_requester)
        #
        # index_event_requested_reviewer = get_index(list(issue_event['requested_reviewer']), user_id)
        # event_requested_reviewer_s = len(index_event_requested_reviewer)

        event_create.append(event_create_c)
        event_assign_collaborator.append(event_assign_collaborator_c)
        event_setting_assignee.append(event_setting_assignee_c)
        event_change_issue_state.append(event_change_issue_state_c)
        event_comment.append(event_comment_c)
    event_active = pd.DataFrame({
        'user_login': user_list,

        'event_create': event_create,
        'event_comment': event_comment,
        'event_assign_collaborator': event_assign_collaborator,
        'event_setting_assignee': event_setting_assignee,
        'event_closed_issue': event_change_issue_state,
    })
    # event_labled, event_referenced, event_mentioned, event_closed, \
    #            event_event_assignee, event_event_assigner, \
    #            event_review_requested, event_ready_for_review
    return event_active
