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
        await session.get(url) # загружаем страницу с найденными вакансиями
        list_of_url = await session.get_elements(keyword) # получаем список объектов по ключевому слову
        new_list = []
        for item in list_of_url:
            element_2 = await item.get_attribute('href') # получаем ссылку из объекта
            new_list.append(element_2)
        pool[url] = new_list   # записываем в пул список вакансий по ссылке


async def run(data_list):
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    tasks = []
    async with get_session(service, browser) as session:
        for data in data_list:
            task = asyncio.ensure_future(fetch(data))  # назначаем таск в виде метода fetch
            tasks.append(task) # добавляем таск в список назначенных тасков
        responses = asyncio.gather(*tasks) # создаем список тасков для выполнения
        await responses
    return responses


t0 = time()
loop = asyncio.get_event_loop() # создаем событийный цикл
asyncio.set_event_loop(loop) # задаем событийный цикл
task = asyncio.ensure_future(run(data_list)) # назначаем таск в виде метода run()
loop.run_until_complete(task) # проводим пока все таски не будут выполнены
#result = task.result().result()

print(pool)
print('total time ASYNCH:', time() - t0)
