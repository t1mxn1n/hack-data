from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['Hack']

collection = db['kommersant']
collection_vcru = db['vcru']

collection_posts = db['posts']


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
    return collection_posts.find({'Source': 'kommersant', 'Comments': {'$gt': avg_comments_k}, 'er': {'$gt': avg_er_k}}).sort([('er', -1)]).limit(1000).sort([('Views', -1)])


def get_posts_vcru(avg_comments_vc, avg_er_vc):
    return collection_posts.find(
        {'Source': 'kommersant', 'Comments': {'$gt': avg_comments_vc}, 'er': {'$gt': avg_er_vc}}).sort(
        [('er', -1)]).limit(1000).sort([('Views', -1)])

