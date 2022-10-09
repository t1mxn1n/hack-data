import time
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from loguru import logger
import csv

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0')
options.add_argument('--disable-blink-features=AutomationControlled')

pages = 13
url_main = 'https://www.biznet.ru/forum/31-drugie-voprosy-nachinayuschih-predprinimateley/page/{page}/?sortby=views&sortdirection=desc'


def main():
    first = True
    try:
        for i in tqdm(range(1, pages)):
            url = url_main.format(page=i)
            driver = webdriver.Chrome(options=options, desired_capabilities=caps)
            driver.get(url)
            time.sleep(1)
            # WebDriverWait(driver, 7).until(EC.presence_of_element_located(
            #    (By.CLASS_NAME, 'sharing')))
            topics = driver.find_elements(by=By.CLASS_NAME, value='ipsDataItem_main')[:-10]
            if first:
                action = 'w'
            else:
                action = 'a'
            with open('role_businessman_2.csv', action, encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                if first:
                    writer.writerow(('discussion', 'role'))
                    first = False
                for topic in topics:
                    t = topic.find_element(by=By.CLASS_NAME, value='ipsDataItem_title').text
                    try:
                        int(t)
                        continue
                    except:
                        s = re.sub(r"\d+", "", t)
                        s = re.sub("^\s+|\n|\r|\s+$", '', s)
                        writer.writerow((str(s), 0))
                driver.close()
                driver.quit()

    except Exception as e:
        logger.error(f'Error in data scraping: {e}')
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
