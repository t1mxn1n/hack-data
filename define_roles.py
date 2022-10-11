from loguru import logger
import pickle


from database import *

ROLES = {
    0: 'businessman',
    1: 'accountant'
}

filename = 'model_v1.pk'
kommersant_url = 'https://www.kommersant.ru/doc/'


def main():
    with open(filename, 'rb') as f:
        loaded_model = pickle.load(f)
    posts_kommerasnt = get_posts()
    counter = 0
    for post in posts_kommerasnt:
        body = post['Body']
        if body == '':
            continue
        role = int(loaded_model.predict([body])[0])
        views = post['Views']
        if "K" in views:
            views = int(views.replace('K', '')) * 1000
        elif 'M' in views:
            views = float(views.replace('M', '').replace(',', '.')) * 1000000
        else:
            views = int(views)
        comments = post['Comments']
        if comments == '':
            comments = 0
        else:
            try:
                comments = int(comments)
            except ValueError:
                comments = 0
        er = comments / views * 100
        source_link = kommersant_url + str(post['DocsID'])
        add_post_general({'Title': post['Title'],
                          'Body': body,
                          'Time': post['Time'],
                          'Comments': comments,
                          'er': er,
                          'role': role,
                          'Views': views,
                          'Link': source_link,
                          'Trend': '',
                          'Source': 'kommersant'})
        counter += 1
        if counter >= 1000:
            logger.info('1000 записей добавилось в бд (kommersant)')
            counter = 0

    posts_vc = get_posts_vc()
    counter = 0
    for post in posts_vc:
        body = post['Body']
        if body == '':
            continue
        role = int(loaded_model.predict([body])[0])
        views = post['Views']
        comments = post['Comments']
        likes = post['Likes']
        er = (comments + likes) / views * 100
        add_post_general({'Title': post['Title'],
                          'Body': body,
                          'Time': post['Time'],
                          'Comments': comments,
                          'er': er,
                          'role': role,
                          'Views': views,
                          'Link': post['Link'],
                          'Trend': '',
                          'Source': 'vc'})
        counter += 1
        if counter >= 1000:
            logger.info('1000 записей добавилось в бд (vc.ru)')
            counter = 0


def get_average_stats():
    data = get_posts_general()
    er_vc = 0
    er_k = 0
    views_k = 0
    views_vc = 0
    counter = 0
    comments_k = 0
    comments_vc = 0
    for post in data:
        if 'kommersant' in post['Link']:
            er_k += post['er']
            views_k += post['Views']
            comments_k += post['Comments']
        else:
            er_vc += post['er']
            views_vc += post['Views']
            comments_vc += post['Comments']
        counter += 1

    avg_er_k = er_k / counter
    avg_views_k = views_k / counter
    avg_comments_k = comments_k / counter
    print('[kommersant]\nAverage er: ', avg_er_k)
    print('Average views: ', avg_views_k)
    print('Average comments: ', avg_comments_k)

    avg_er_vc = er_vc / counter
    avg_views_vc = views_vc / counter
    avg_comments_vc = comments_vc / counter
    print('[vc]\nAverage er: ', avg_er_vc)
    print('Average views: ', avg_views_vc)
    print('Average comments: ', avg_comments_vc)

    kommersant_data = get_posts_kommersant(avg_comments_k, avg_er_k)
    list_k = []
    for post_k in kommersant_data:
        list_k.append(post_k)

    vc_data = get_posts_vcru(avg_comments_vc, avg_er_vc)
    list_vc = []
    for post_vc in vc_data:
        list_vc.append(post_vc)

    for i in list_vc:
        if i not in list_k:
            list_k.append(i)

    newlist = sorted(list_k, key=lambda d: d['er'])
    add_sorted_data(newlist)
    return newlist


if __name__ == '__main__':
    main()
    get_average_stats()

# 0.5260641189098968
# 11258.20954857886
