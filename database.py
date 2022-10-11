import math

from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('mongodb://localhost:27017/')

db = client['Hack']

collection = db['kommersant']
collection_vcru = db['vcru']

collection_posts = db['posts']
collection_sorted = db['sorted_data']


def add_post(post, data):
    collection.insert_one({'Title': post['Title'],
                           'Body': data['body'],
                           'Time': int(post['DateBegin']),
                           'DocsID': post['DocsID'],
                           'Comments': data['comments'],
                           'Views': data['views']})


def get_posts():
    data = collection.find()
    return data


def drop_db():
    collection.drop()


def add_post_vc(post):
    collection_vcru.insert_one({'Title': post['Title'],
                                'Body': post['Body'],
                                'Time': post['Time'],
                                'Comments': post['Comments'],
                                'Likes': post['Likes'],
                                'Views': int(post['Views']),
                                'Link': post['Link']})


def get_posts_vc():
    data = collection_vcru.find()
    return data


def drop_db_vc():
    collection_vcru.drop()


def add_post_general(post):
    collection_posts.insert_one({'Title': post['Title'],
                                 'Body': post['Body'],
                                 'Time': post['Time'],
                                 'Comments': post['Comments'],
                                 'er': post['er'],
                                 'role': post['role'],
                                 'Views': post['Views'],
                                 'Link': post['Link'],
                                 'Trend': '',
                                 'Source': post['Source']})


def get_posts_general():
    data = collection_posts.find()
    return data


def drop_db_general():
    collection_posts.drop()


def get_posts_kommersant(avg_comments_k, avg_er_k):
    return collection_posts.find(
        {'Source': 'kommersant', 'Comments': {'$gt': avg_comments_k}, 'er': {'$gt': avg_er_k}}).sort(
        [('er', -1)]).limit(1000).sort([('Views', -1)])


def get_posts_vcru(avg_comments_vc, avg_er_vc):
    return collection_posts.find(
        {'Source': 'vc', 'Comments': {'$gt': avg_comments_vc}, 'er': {'$gt': avg_er_vc}}).sort(
        [('er', -1)]).limit(1000).sort([('Views', -1)])


def get_sorted_data(role):
    data = collection_sorted.find(
        {'role': role},
        {'_id': 0,
         'Title': 1,
         'Time': 1,
         'Comments': 1,
         'Body': 1,
         'er': 1,
         'role': 1,
         'Views': 1,
         'Link': 1,
         'Source': 1
         }
    ).sort([('Views', -1)])
    result = {}
    for index, value in enumerate(data):
        if index == 3:
            break
        result.update({str(index): value})
    return result


def add_sorted_data(data):
    collection_sorted.delete_many({})
    collection_sorted.insert_many(data)


def get_sorted_data_by_source_with_role(source, role):
    data = collection_sorted.find(
        {'Source': source,
         'role': role},
        {'_id': 0,
         'Title': 1,
         'Time': 1,
         'Comments': 1,
         'Body': 1,
         'er': 1,
         'role': 1,
         'Views': 1,
         'Link': 1,
         'Source': 1
         }
    ).sort([('Views', -1)])
    result = {}
    for index, value in enumerate(data):
        if index == 3:
            break
        result.update({str(index): value})
    return result


def get_sorted_data_by_source(source):
    data = collection_sorted.find(
        {'Source': source},
        {'_id': 0,
         'Title': 1,
         'Time': 1,
         'Comments': 1,
         'Body': 1,
         'er': 1,
         'role': 1,
         'Views': 1,
         'Link': 1,
         'Source': 1
         }
    ).sort([('Views', -1)])
    result = {}
    for index, value in enumerate(data):
        if index == 3:
            break
        result.update({str(index): value})
    return result


def get_trends():
    time_now = datetime.now()
    timestamp_delta = math.ceil(
        datetime.timestamp(time_now - timedelta(days=21))
    )

    data1 = collection_sorted.find(
        {'Source': 'kommersant', 'Time': {'$gt': timestamp_delta}},
        {'_id': 0,
         'Title': 1,
         'Time': 1,
         'Comments': 1,
         'Body': 1,
         'er': 1,
         'role': 1,
         'Views': 1,
         'Link': 1,
         'Source': 1
         }
    ).sort([('Comments', -1)])
    result = {}
    for index, value in enumerate(data1):
        if index == 2:
            break
        result.update({str(index): value})

    data2 = collection_sorted.find(
        {'Source': 'vc', 'Time': {'$gt': timestamp_delta}},
        {'_id': 0,
         'Title': 1,
         'Time': 1,
         'Comments': 1,
         'Body': 1,
         'er': 1,
         'role': 1,
         'Views': 1,
         'Link': 1,
         'Source': 1
         }
    ).sort([('Comments', -1)])
    for index, value in enumerate(data2, start=2):
        if index == 4:
            break
        result.update({str(index): value})
    return result


def get_insights():
    time_now = datetime.now()
    timestamp_delta = math.ceil(
        datetime.timestamp(time_now - timedelta(days=150))
    )
    data = collection_vcru.find(
        {'Time': {'$gt': timestamp_delta}},
        {'_id': 0,
         'Title': 1,
         'Time': 1,
         'Comments': 1,
         'Body': 1,
         'Likes': 1,
         'Views': 1,
         'Link': 1
         }
    ).sort([('Likes', -1)])
    result = {}
    for index, value in enumerate(data):
        if index == 5:
            break
        result.update({str(index): value})
    return result