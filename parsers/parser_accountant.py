import requests
import csv
from loguru import logger

ROLES = {
    'businessman': 0,
    'accountant': 1,
    'programmers': 2
}

FORUMS = {
    'businessman': 'https://www.biznet.ru/',
    'accountant': 'https://club.klerk.ru/c/accounting/5'
    # 'programmers': 'https://www.cyberforum.ru/blogs/recent-entries/'
}


def accountant():
    news_list, page = list(), 0
    with open(
            '../dataset/role_accountant.csv',
            'w',
            encoding='utf-8',
            newline=''
    ) as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(('discussion', 'role'))
        while page != 800:
            response = requests.get(
                f'https://club.klerk.ru/c/accounting/5.json?page={page}'
            )
            json_topics = response.json()['topic_list']['topics']
            for topic in json_topics:
                dict_data, tags = dict(), str()
                if topic['tags_descriptions'] != {}:
                    for tag in topic['tags_descriptions'].keys():
                        tags += tag + ' ' + topic['tags_descriptions'][tag] + ' '
                else:
                    tags = ''
                dict_data.update({
                    'discussion': topic['title'] + ' ' + tags,
                    'role': ROLES['accountant']
                })
                writer.writerow((dict_data['discussion'], dict_data['role']))
            logger.info(f'Parsed page: {page}')
            page += 1
    return news_list


if __name__ == '__main__':
    accountant()
