from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['Hack']

collection = db['kommersant']


def add_post(post, data):
    collection.insert_one({'Title': post['Title'],
                           'Body': data['body'],
                           'Time': int(post['DateBegin']),
                           'DocsID': post['DocsID'],
                           'Comments': data['comments'],
                           'Views': data['views']})


def get_posts():
    data = collection.find().sort('Time', -1)
    return data


def drop_db():
    collection.drop()
