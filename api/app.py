from flask import Flask, jsonify

from database import get_sorted_data, get_sorted_data_by_source, get_sorted_data_by_source_with_role, get_trends, get_insights

app = Flask(__name__)


@app.route("/role/0")
def find_news_businessman():
    data = get_sorted_data(0)
    return jsonify(**data)


@app.route("/role/1")
def find_news_accountant():
    data = get_sorted_data(1)
    return jsonify(**data)


@app.route("/source/vc")
def find_news_vc():
    data = get_sorted_data_by_source('vc')
    return jsonify(**data)


@app.route("/source/vc/0")
def find_news_vc_0():
    data = get_sorted_data_by_source_with_role('vc', 0)
    return jsonify(**data)


@app.route("/source/vc/1")
def find_news_vc_1():
    data = get_sorted_data_by_source_with_role('vc', 1)
    return jsonify(**data)


@app.route("/source/kommers")
def find_news_kommers():
    data = get_sorted_data_by_source('kommersant')
    return jsonify(**data)


@app.route("/source/kommers/0")
def find_news_kommers_0():
    data = get_sorted_data_by_source_with_role('kommersant', 0)
    return jsonify(**data)


@app.route("/source/kommers/1")
def find_news_kommers_1():
    data = get_sorted_data_by_source_with_role('kommersant', 1)
    return jsonify(**data)


@app.route("/trends")
def find_trends():
    data = get_trends()
    return jsonify(**data)


@app.route("/insights")
def find_insights():
    data = get_insights()
    return jsonify(**data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=10010)
