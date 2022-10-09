from flask import Flask
from pymongo import MongoClient
import json


client = MongoClient('mongodb://localhost:27017/')
db_testing = client['testing_tfm']
collection_testing = db_testing['coinhall_tests']
app = Flask(__name__)


def find_data(address):
    data = collection_testing.find_one(
        {'address': address},
        {'_id': 0,
        'address': 1,
        'timestamp': 1,
        'market_cap_diff': 1,
        'fdv_diff': 1,
        'liquidity_diff': 1,
        'volume_diff': 1,
        'apr_diff': 1,
        'price_diff': 1,
        'price24h_diff': 1,
        'coinhall': {'chain': 1}
        }
    )
    return data


@app.route("/role/0")
def find_news_businessman():
    address = 'terra1fd68ah02gr2y8ze7tm9te7m70zlmc7vjyyhs6xlhsdmqqcjud4dql4wpxr'
    data = find_data(address)
    return json.dumps(data)


@app.route("/role/1")
def find_news_accountant():
    address = 'terra1ygn5h8v8rm0v8y57j3mtu3mjr2ywu9utj6jch6e0ys2fc2pkyddqekwrew'
    data = find_data(address)
    return json.dumps(data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=10010)
