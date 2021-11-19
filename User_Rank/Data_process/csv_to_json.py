import csv
import json
import pandas as pd
import numpy
from elasticsearch import Elasticsearch
# csv文件转换为json文件

def csv2json(path, savepath, filenames):
    csvfile = open(path, 'r')
    jsonfile = open(savepath, 'w')
    # jsonfile = 'issue_data.json'
    reader = csv.DictReader(csvfile, filenames)
    for row in reader:
        # print(row['title_spilt'])
        # row['title_spilt'] = eval(row['title_spilt'])
        json.dump(row, jsonfile, ensure_ascii=False)
        jsonfile.write('\n')
    return jsonfile


def csv2json1(path):
    js = json.loads('{"\u6728\u6613\u67d0\u95f2\u4eba":"中国"}')
    data = pd.read_csv(path)
    columns = list(data)
    savepath = path[0:-4] + '1.json'
    csv2json(path, savepath, columns)


def csv2json2(path):
    import json
    import csv
    js = json.loads('{"\u6728\u6613\u67d0\u95f2\u4eba":"中国"}')
    primary_fields = ['community_name', 'issue_id', 'title', 'body', 'issue_url', 'assignee', 'creator', 'comments',
                      'created_at']
    result = []
    jsonfile = open(path[0:-4] + '.json', 'w')

    with open(path) as csv_file:
        reader = csv.DictReader(csv_file, skipinitialspace=True)
        for row in reader:
            d = {k: v for k, v in row.items() if k in primary_fields}
            for k, v in row.items():
                if k not in primary_fields:
                    if len(eval(v)) == 0 or len(eval(v)) == 1:
                        d[k] = eval(v)
                    else:
                        temp = []
                        for i in eval(v):
                            temp.append(i[0])
                        d[k] = temp
                        # d[k] = sorted(eval(v))
            result.append(d)
            json.dump(d, jsonfile, ensure_ascii=False)
            jsonfile.write('\n')

    # result = json.dumps(result,indent=2, ensure_ascii=False)

    # f2 = open(path[0:-4] + '.json', 'w')
    # f2.write(result)
    # f2.close()


if __name__ == '__main__':
    # path = '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_comment.csv'
    # path = '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/数据分析/community_title.csv'
    # path = '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/Data_Crawel/Community_Issue_Data/All_data/Openeuler+Src_all_issue_data.csv'
    # path = '/Users/wenzong/PycharmProjects/OpenEuler-用户画像/数据分析/user_tf_idf.csv'
    path = '/User_Rank/event_data/tensorflow_issue_event_0916_login.csv'
    csv2json1(path)
    # csv2json2(path)

    # es = Elasticsearch([{"host": "localhost", "port": 9200}])
    # # # # 创建字段
    # body_daily_close = {
    #     "mappings": {
    #         "properties": {
    #             "comment_label(rule)": {
    #                 "type": "keyword"
    #             }
    #         }
    #     }
    # }
    # properties = body_daily_close.get("mappings").get("properties")
    # es.indices.put_mapping(index='all_issue_comment', body=body_daily_close.get("mappings"))
