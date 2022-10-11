import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from loguru import logger

from database import add_post_vc

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0')
options.add_argument('--disable-blink-features=AutomationControlled')

url_main = 'https://vc.ru/companies/new'


def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))


def get_links():
    driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    url = url_main
    driver.get(url)
    try:
        data = []
        time_5min = datetime.now() + timedelta(minutes=5)
        while time_5min > datetime.now():
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        items = driver.find_elements(by=By.CLASS_NAME, value='feed__item')
        for item in items:
            i = item.find_element(by=By.CLASS_NAME, value='content-link').get_attribute('href') + ' \n'
            data.append(i)
        uniq = list(set(data))
        print(len(data))
        print(len(uniq))
        print(len(data) - len(uniq))
        with open('links_v3.txt', 'w') as file:
            file.writelines(uniq)
    except Exception as e:
        logger.error(f'Error in data scraping: {e}')
    finally:
        driver.close()
        driver.quit()


def get_data(links):
    for link in tqdm(links):
        try:
            r = requests.get(url=link)
            soup = BeautifulSoup(r.text, 'html.parser')
            info = soup.find(class_='l-hidden entry_data').get('data-article-info')
            data = json.loads(info)
            views = soup.find(class_='views__value').text.replace(' ', '')
            views = get_num(views)
            title_s = soup.find(class_='content-title')
            title = title_s.text.strip().replace('Статьи редакции', '').replace('\n', '')
            time_create = soup.find(class_='time').get('title').replace(' (Europe/Moscow)', '').replace('.', '/')
            date_sample = "%d/%m/%Y %H:%M:%S"
            time_create = int(datetime.strptime(time_create, date_sample).timestamp())
            content = soup.find(class_='content content--full')
            partial_content = str(content).split('<div class="block-delimiter"></div>')
            final_body = partial_content[0].split('<div class="content-info__item content-info__item--right">')
            body = BeautifulSoup(final_body[-1], 'html.parser')
            text = body.find_all(class_='l-island-a')
            res = ''
            for b in text:
                res += b.text.strip().replace('\n', '')
            add_post_vc({
                'Title': title,
                'Body': res,
                'Time': time_create,
                'Comments': data['comments'],
                'Likes': data['likes'],
                'Views': views,
                'Link': link
            })
        except Exception:
            logger.error(f'Ошибка в {link}')
            continue


def main():
    time_start = datetime.now()
    links = []
    with open('links_v3.txt', 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            links.append(line.replace(' \n', ''))

    part = len(links) // 3
    # posts = [posts[0:part], posts[part: part * 2], posts[part * 2: part * 3], posts[part * 3:]]
    links = [links[0:part], links[part: part * 2], links[part * 2:]]
    p = Pool(processes=3)
    p.map(get_data, links)

    time_end = datetime.now()
    logger.info(f'Данные собраны за {time_end - time_start}')


if __name__ == '__main__':
    get_links()
    main()
