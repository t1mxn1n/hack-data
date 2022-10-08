from bs4 import BeautifulSoup
import requests
from pyppeteer import launch
import asyncio


PAGING = '&page=%d'
PAGE_XPATH = '//*[@id="elPagination_db90c3d4a47e43e1de84107744179b6d_1211677790"]/li[10]'

URLS = {
    'news': 'https://www.biznet.ru/forum/94-biznes-v-sfere-uslug'
}

# HEADERS = {
#     'authority': 'mc.yandex.ru',
#     'method': 'POST',
#     'scheme': 'https',
#     'accept': '*/*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'ru,en;q=0.9',
#     'content-length': '530',
#     'content-type': 'text/plain',
#     'cookie': 'yandexuid=7522746131656867885; yuidss=7522746131656867885; ymex=1972227887.yrts.1656867887#1972227886.yrtsi.1656867886; gdpr=0; _ym_uid=16568678871073595664; yandex_login=leznevskiy@mail.ru; my=YwA=; _ym_d=1662744220; i=FdrjB+wCLsc7AdV0J27Kv80XekwPbW3g2iVbJzO0Qe9U+XUcgiq/0Ec37+CVwKk06tiC5zKAGAOsvI5+xDlzcvRS8yA=; yabs-frequency=/5/000D0000001X3ZjZ/IkQnfDqwfKR4I2u0/; is_gdpr=0; is_gdpr_b=COvZDxDpjQEoAg==; Session_id=3:1665130141.5.0.1656868000151:hLl7bQ:2d.1.2:1|1141641184.0.2|3:10259329.661998.Ki0IAYeb9yWAYiPSn8fM16bc_6o; sessionid2=3:1665130141.5.0.1656868000151:hLl7bQ:2d.1.2:1.499:1|1141641184.0.2|3:10259329.587530.fakesign0000000000000000000; sae=0:CB254EDC-B650-4CC7-8DA7-9740D3D866AF:p:22.9.2.1495:w:d:RU:20220703; _ym_isad=2; yabs-sid=1939881751665203330; cycada=qQ1KHuwQpqCokS/ZSAB0+kpZtwTCVEjyu3aoT8zCoS4=; yp=1665288090.uc.ru#1665288090.duc.ru#1688403887.brd.0702004871#1688403887.cld.2270452#1972228000.udn.cDpsZXpuZXZza2l5QG1haWwucnU%3D#1688452307.stltp.serp_bk-map_1_1656916307#1665422632.csc.1#1974544279.hks.0#1980589723.pcs.1#1979910332.dark_promo.5#1696481619.pgp.2_27749042#1679364707.szm.1:1920x1080:1920x950#1665239491.gpauto.56_484638:84_947647:100000:3:1665232291#1665547377.mcv.0#1665547377.mcl.au919f; sync_cookie_csrf=707156450fake',
#     'origin': 'https://www.biznet.ru',
#     'referer': 'https://www.biznet.ru/',
#     'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Yandex";v="22"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': "Windows",
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'
# }


# async def get_business_pages():
#     browser = await launch(
#         options={'args': ['--no-sandbox']}
#     )
#     context_incognito = await browser.createIncognitoBrowserContext()
#     page = await context_incognito.newPage()
#     await page.goto(url=URLS['service'])
#     data = await page.content()
#     if data.find('ipsPagination_last') != -1:
#         print(data)
#     # data = await page.xpath(PAGE_XPATH)
#     # data = await page.evaluate('el => el.textContent', data)
#     await browser.close()
#     # print(data)


def get_business_pages():
    response = requests.get(
        url='https://forumbusiness.net/forumdisplay.php?f=97&order=desc&page=3'
        # headers=HEADERS
    )
    text = response.text
    # if text.find('ipsPagination_last') != -1:
    #     print(text)
    soup = BeautifulSoup(text, 'html.parser')
    find_bs4 = soup.find_all(class_='threadbit hot')
    for value in find_bs4:
        print(value)
    #     td_threadstatusicon = value.get('id')
    #     if (
    #         td_threadstatusicon != None and
    #         td_threadstatusicon.find('td_threadstatusicon_') != -1
    #     ):
    #         print(td_threadstatusicon.replace('td_threadstatusicon_', ''))
    # soup = BeautifulSoup(r.text, 'html.parser')
    # texts = soup.find_all(class_='doc__text')[:-1]
    # sharing = soup.find(class_='doc_sharing__body js-social')
    # # print(sharing)
    # for text in texts:
    #     if 'doc__text document_authors' in str(text):
    #         continue
    #     result += text.text + ' '
    # add_post(post, result)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_business_pages())
    get_business_pages()