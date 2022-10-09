import time

import requests
from datetime import datetime
from loguru import logger
from multiprocessing import Process, Pool
from threading import Thread
from bs4 import BeautifulSoup

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from database import add_post, drop_db

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()

first_url = 'https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=1&listid={type_data}&date=&intervaltype=&page=1'
second_url = 'https://www.kommersant.ru/listpage/lazyloaddocs?regionid=77&listtypeid=1&listid={type_data}&date=&intervaltype=4&idafter={id}'
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


types_data = {'finance': 40, 'business': 4}


def get_pages(type_):
    data = []
    r = requests.get(url=first_url.format(type_data=type_), headers=headers)
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
        r = requests.get(url=second_url.format(type_data=type_, id=next_page_id))
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
        if counter == 50:
            logger.info(f'+{50 * 20} постов......')
            counter = 0
        if int(data[-1]['DateBegin']) < timestamp_parse:
            break

    logger.info(f'Собранно {len(data)} постов, последний пост: {data[-1]}')
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


def get_data_from_post_by_webdriver(posts):
    driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    try:
        for post in tqdm(posts):
            url = url_main + str(post['DocsID'])
            driver.get(url)
            WebDriverWait(driver, 7).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'sharing')))
            views = driver.find_elements(by=By.CLASS_NAME, value='sharing')
            user_views = views[0].text
            comments = views[1].text
            body = driver.find_elements(by=By.CLASS_NAME, value='doc__text')[:]
            text_body = ''
            for item in body:
                if item.get_attribute(name='class') == 'doc__text document_authors':
                    continue
                text_body += item.text
            add_post(post, {'views': user_views, 'comments': comments, 'body': text_body})
    except Exception as e:
        logger.error(f'Error in data scraping: {e}')
    finally:
        driver.close()
        driver.quit()


def main(type_):
    time_start = datetime.now()
    posts = get_pages(type_)
    part = len(posts) // 3
    # posts = [posts[0:part], posts[part: part * 2], posts[part * 2: part * 3], posts[part * 3:]]
    posts = [posts[0:part], posts[part: part * 2], posts[part * 2:]]
    p = Pool(processes=3)
    p.map(get_data_from_post_by_webdriver, posts)
    # for post in posts:
    #     get_data_from_post_by_webdriver(post)

    time_end = datetime.now()
    logger.info(f'Данные собраны за {time_end - time_start}')


if __name__ == '__main__':
    # 'business' 'finance'
    type_data = 'finance'
    main(types_data[type_data])
    # u = 'https://tns-counter.ru/e/ec01&cid=kommersant_ru&typ=1&tms=kommersant_ru&idc=155&uid=r4yoydl35z9g2c2i&hid=&idlc=5549514&ver=0&type=4'
    # r = requests.get(url=u, headers=headers)
    # print(r.text)

