import asyncio
import sys
from time import time
from arsenic import get_session, keys, browsers, services
#import models
#from models import HeadHunter, MoiKrug, Session
from contextlib import contextmanager, asynccontextmanager
from models1 import HeadHunter, MoiKrug, engine
from sqlalchemy.schema import CreateTable, DropTable
from sqlalchemy_aio import ASYNCIO_STRATEGY

@contextmanager
async def connect():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


async def fetch_MK_links():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        await session.get('https://moikrug.ru/vacancies?q=3d+s+max&sort=date&currency=rur&with_salary=1')
        list_of_links = await session.get_elements('a[class=job_icon]') # получаем список линков

        print('len(list_of_links)', len(list_of_links))
        list_of_titles = await session.get_elements('div[class=title]')  # 'a[class=job_icon]'
        filtred_list_of_titles = []
        for item in list_of_titles:
            title = await item.get_attribute('title')
            if title != None:
                filtred_list_of_titles.append(title)  # получаем отфильтрованный список названий вакансий
        banner_vacancy = await session.get_element('div[class=vacancy_banner]') # проверяем есть ли рекламная вакансия в баннере
                                                                                # если есть - из в итоговый список типов занятости заносим
                                                                                # элемент, начиная с первого
        banner_content =  await banner_vacancy.get_text()
        if banner_content == None:
            summand = 0
        else:
            summand = 1

        list_of_compensations = await session.get_elements('div[class=count')  # 'a[class=job_icon]'
        list_of_skills = await session.get_elements('div[class=skills]')
        list_of_companies = await session.get_elements('span[class=company_name]')
        list_of_occupations = await session.get_elements('span[class=occupation]')
        new_list = []
        for i in range(len(list_of_links)):
            link = await list_of_links[i].get_attribute('href')  # получаем ссылку
            link = 'https://moikrug.ru' + link
            new_list.append([link])  # добавляем ссылку
            new_list[i].append(filtred_list_of_titles[i])  # добавляем название вакансии
            compensation = await list_of_compensations[i].get_text()  # получаем размер зарплаты
            new_list[i].append(compensation)  # добавляем размер зарплаты
            skills = await list_of_skills[i].get_text()  # получаем список навыков
            new_list[i].append(skills)  # добавляем список навыков
            company = await list_of_companies[i].get_text()  # получаем название компании
            new_list[i].append(company)  # добавляем название компании
            occupation = await list_of_occupations[i].get_text()  # получаем тип занятости
            new_list[i].append(occupation)  # добавляем тип занятости
        pool['moi_krug_list'] = new_list


async def fetch_MK_content():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    await engine.execute(CreateTable(MoiKrug))
    conn = await engine.connect()
    async with get_session(service, browser) as web_session:
        for i in range(len(pool['moi_krug_list'])):
            await web_session.get(pool['moi_krug_list'][i][0])
            description_object = await web_session.get_element('div[class=vacancy_description]')
            description = await description_object.get_text()
            #pool['moi_krug_list'][i].append(description)
            print('DESCRIPTION:', description)
            link = pool['moi_krug_list'][i][0]
            title = pool['moi_krug_list'][i][1]
            salary = pool['moi_krug_list'][i][2]
            skills = pool['moi_krug_list'][i][3]
            company = pool['moi_krug_list'][i][4]
            occupation = pool['moi_krug_list'][i][5]
            await conn.execute(MoiKrug.insert().values(link=link, title=title, salary=salary,
                                                          skills=skills,
                                                          company=company,
                                                          occupation=occupation,
                                                          description=description))
        await conn.close()



async def fetch_HH_links():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        await session.get('https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true')
        list_of_titles = await session.get_elements('a[data-qa=vacancy-serp__vacancy-title]')  # 'a[class=job_icon]'
        list_of_compensations = await session.get_elements('div[data-qa=vacancy-serp__vacancy-compensation]')  # 'a[class=job_icon]'
        list_of_responsibilities = await session.get_elements('div[data-qa=vacancy-serp__vacancy_snippet_responsibility]')
        list_of_requirements = await session.get_elements('div[data-qa=vacancy-serp__vacancy_snippet_requirement]')
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
        pool['headhunter_list'] = new_list


async def fetch_HH_content():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    await engine.execute(CreateTable(HeadHunter))
    conn = await engine.connect()
    async with get_session(service, browser) as web_session:
        for i in range(len(pool['headhunter_list'])): # идем поэлементно по списку линков
            await web_session.get(pool['headhunter_list'][i][0])  # загражаем линк из списка
            company_object = await web_session.get_element('span[itemprop=name]')
            company = await company_object.get_text()
            # location_object = await session.get_element('span[itemprop=jobLocation]')
            # location = await location_object.get_text()
            experience_object = await web_session.get_element('span[data-qa=vacancy-experience]')
            experience = await experience_object.get_text()
            employment_mode_object = await web_session.get_element('p[data-qa=vacancy-view-employment-mode]')
            employment_mode = await employment_mode_object.get_text()
            description_object = await web_session.get_element('div[data-qa=vacancy-description')
            description = await description_object.get_text()
            #description = description_object.get_text()
            link = pool['headhunter_list'][i][0]
            title = pool['headhunter_list'][i][1]
            salary = pool['headhunter_list'][i][2]
            responsibilites_short = pool['headhunter_list'][i][3]
            requirements_short = pool['headhunter_list'][i][4]
            await conn.execute(HeadHunter.insert().values(link=link, title=title, salary=salary,
                                                          responsibilites_short=responsibilites_short,
                                                          requirements_short=requirements_short,
                                                          company=company,
                                                          experience=experience,
                                                          employment_mode=employment_mode,
                                                          description=description))
        await conn.close()





async def start_method(method_gets_links, method_gets_content):
    mytask_1 = asyncio.create_task(method_gets_links)  # проводим пока все таски не будут выполнены
    await mytask_1
    mytask_2 = asyncio.create_task(method_gets_content)
    await mytask_2


async def run_1(data_list):
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    tasks = []
    async with get_session(service, browser) as session:
        for data in data_list:
            task = asyncio.ensure_future(start_method(data[0],data[1]))  # назначаем таск в виде метода fetch
            tasks.append(task) # добавляем таск в список назначенных тасков
        responses = asyncio.gather(*tasks) # создаем список тасков для выполнения
        await responses
    return responses


if sys.platform.startswith('win'):
    GECKODRIVER = './geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'

pool = {}

a = fetch_HH_links()
b = fetch_HH_content()
c = fetch_MK_links()
d = fetch_MK_content()


data_list=[[a,b],[c,d]]


if __name__ == '__main__':
    t0 = time()
    asyncio.run(run_1(data_list))
    print("total pool:", pool)
    print('total time SYNCH:', time() - t0)


