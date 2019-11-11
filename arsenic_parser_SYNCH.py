import asyncio
import sys
from time import time
from arsenic import get_session, keys, browsers, services

if sys.platform.startswith('win'):
    GECKODRIVER = './geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'


pool = {}


data_1 = {'url': 'https://moikrug.ru/vacancies?q=3d+s+max&sort=date&currency=rur&remote=1',
            'keyword':  'a[class=job_icon]' }
data_2 = {'url': 'https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=113&text=Python&enable_snippets=true',
          'keyword': 'a[data-qa=vacancy-serp__vacancy-title]'}


data_list =[data_1, data_2]

async def fetch(data):
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    url = data['url']
    keyword = data['keyword']
    async with get_session(service, browser) as session:
        await session.get(url)
        list_of_url = await session.get_elements(keyword) # 'a[class=job_icon]'
        new_list = []
        for item in list_of_url:
            element_2 = await item.get_attribute('href')
            new_list.append(element_2)
        pool[url] = new_list


def main():
    loop = asyncio.get_event_loop() # создаем событийный цикл
    loop.run_until_complete(fetch(data_1)) # проводим пока все таски не будут выполнены
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch(data_2))


if __name__ == '__main__':
    t0 = time()
    main()
    print("total pool:", pool)
    print('total time SYNCH:', time() - t0 )
