import requests
from datetime import datetime
from loguru import logger
from multiprocessing import Pool
from bs4 import BeautifulSoup

from database import add_post, drop_db

first_url = 'https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=1&listid=40&date=&intervaltype=&page=1'
second_url = 'https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=1&listid=40&date=&intervaltype=3&idafter={id}'
url_main = 'https://www.kommersant.ru/doc/'

headers = {
    'Host': 'www.kommersant.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.kommersant.ru/finance?from=burger&page=2',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
# 1602099966 : 2 years
timestamp_parse = 1602099966


def get_pages():
    data = []
    r = requests.get(url=first_url, headers=headers)
    first_20 = r.json()['Items']
    for page in first_20:
        data.append({
            'DocsID': page['DocsID'],
            'DateBegin': page['DateBegin'].split('/Date(')[1].split(')/')[0],
            'Title': page['Title']
        })

    first = True
    counter = 0
    while True:
        counter += 1
        if first:
            next_page_id = first_20[-1]['DocsID']
            first = False
        r = requests.get(url=second_url.format(id=next_page_id))
        posts = r.json()['Items']
        for page in posts:
            data.append({
                'DocsID': page['DocsID'],
                'DateBegin': page['DateBegin'].split('/Date(')[1].split(')/')[0],
                'Title': page['Title']
            })
        try:
            next_page_id = posts[-1]['DocsID']
        except:
            logger.error('While loop is closed.')
            break

        if int(data[-1]['DateBegin']) < timestamp_parse:
            break

    logger.info(f'Собранно {len(data)} постов')
    return data


def get_data_from_post(post):
    result = ''
    url = url_main + str(post['DocsID'])
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    texts = soup.find_all(class_='doc__text')[:-1]
    sharing = soup.find(class_='doc_sharing__body js-social')
    # print(sharing)
    for text in texts:
        if 'doc__text document_authors' in str(text):
            continue
        result += text.text + ' '
    add_post(post, result)


def main():
    time_start = datetime.now()
    posts = get_pages()
    p = Pool(processes=3)
    p.map(get_data_from_post, posts)
    # for post in posts:
    #    get_data_from_post(post)
    time_end = datetime.now()
    logger.info(f'Данные собраны за {time_end - time_start}')


if __name__ == '__main__':
    main()
    # u = 'https://tns-counter.ru/e/ec01&cid=kommersant_ru&typ=1&tms=kommersant_ru&idc=155&uid=r4yoydl35z9g2c2i&hid=&idlc=5549514&ver=0&type=4'
    # r = requests.get(url=u, headers=headers)
    # print(r.text)

