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


async def fetch_MK():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        await session.get('https://moikrug.ru/vacancies?q=3d+s+max&sort=date&currency=rur&with_salary=1')
        list_of_links = await session.get_elements('a[class=job_icon]')
        print ('len(list_of_links)', len(list_of_links))
        list_of_titles = await session.get_elements('div[class=title]') # 'a[class=job_icon]'
        print('len(list_of_titles)', len(list_of_titles))
        list_of_compensations = await session.get_elements('div[class=count')  # 'a[class=job_icon]'
        print('len(list_of_compensations)', len(list_of_compensations))
        list_of_skills = await session.get_elements('div[class=skills]')
        print('len(list_of_skills)', len(list_of_skills))
        list_of_companies = await session.get_elements('span[class=company_name]')
        print('list_of_companies)', len(list_of_links))
        #list_of_locations = await session.get_elements('span[class=location]')
        list_of_occupations = await session.get_elements('span[class=occupation]')
        print('len(list_of_occupations)', len(list_of_occupations))

        new_list = []

        for i in range(len(list_of_titles)):
            title = await list_of_titles[i].get_attribute('title')
            new_list.append(title)

        new_list_2 = []

        for item in list_of_occupations:
            occupation = await item.get_text()
            new_list_2.append(occupation)

        pool['titles'] = new_list
        pool['occupation'] = new_list_2

async def fetch_HH():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    #url = data['url']
    #keyword = data['keyword']
    async with get_session(service, browser) as session:
        await session.get('https://ekaterinburg.hh.ru/search/vacancy?clusters=true&enable_snippets=true&only_with_salary=true&order_by=publication_time&text=Python&area=1&from=cluster_area&showClusters=true')
        list_of_titles = await session.get_elements('a[data-qa=vacancy-serp__vacancy-title]') # 'a[class=job_icon]'
        list_of_compensations = await session.get_elements(
            'div[data-qa=vacancy-serp__vacancy-compensation]')  # 'a[class=job_icon]'
        list_of_responsibilities = await session.get_elements(
            'div[data-qa=vacancy-serp__vacancy_snippet_responsibility]')
        list_of_requirements = await session.get_elements(
            'div[data-qa=vacancy-serp__vacancy_snippet_requirement]')

        new_list = []
        for i in range(len(list_of_titles)):
            link = await list_of_titles[i].get_attribute('href')
            new_list.append([link])
            title = await list_of_titles[i].get_text()
            new_list[i].append(title)
            compensation = await list_of_compensations[i].get_text()
            new_list[i].append(compensation)
            responsibility = await list_of_responsibilities[i].get_text()
            new_list[i].append(responsibility)
            requirements = await list_of_requirements[i].get_text()
            new_list[i].append(requirements)
        pool['headhunter'] = new_list


def main():
    loop = asyncio.get_event_loop() # создаем событийный цикл
    loop.run_until_complete(fetch_MK()) # проводим пока все таски не будут выполнены


if __name__ == '__main__':
    main()
    print("total pool:", pool)
    

