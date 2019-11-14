import asyncio
import sys
from time import time
from arsenic import get_session, keys, browsers, services
import models
from models import HeadHunter, MoiKrug, Session
from contextlib import contextmanager

@contextmanager
def connect():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


async def fetch_MK_content():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        for i in range(len(pool['moi_krug_list'])):
            await session.get(pool['moi_krug_list'][i][0])
            #title_object = await session.get_element('h1[class=title]')
            #title = await title_object.get_text()
            description_object = await session.get_element('div[class=vacancy_description]')
            description = await description_object.get_text()
            #pool['moi_krug_list'][i].append(title)
            pool['moi_krug_list'][i].append(description)


async def fetch_MK_links():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        await session.get('https://moikrug.ru/vacancies?q=3d+s+max&sort=date&currency=rur&with_salary=1')
        list_of_links = await session.get_elements('a[class=job_icon]')

        print ('len(list_of_links)', len(list_of_links))
        list_of_titles = await session.get_elements('div[class=title]') # 'a[class=job_icon]'
        sorted_list_of_titles =[]
        for item in list_of_titles:
            title = await item.get_attribute('title')
            if title != None:
                sorted_list_of_titles.append(title)

        banner_vacancy = await session.get_element('div[class=vacancy_banner]')
        banner_content = await banner_vacancy.get_text()
        if banner_content == None:
            summand = 0
        else:
            summand = 1

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

        for i in range(len(list_of_links)):
            link = await list_of_links[i].get_attribute('href') # получаем ссылку
            link = 'https://moikrug.ru' + link
            new_list.append([link]) # добавляем ссылку
            new_list[i].append(sorted_list_of_titles[i]) # добавляем название вакансии
            compensation = await list_of_compensations[i].get_text() # получаем размер зарплаты
            new_list[i].append(compensation) # добавляем размер зарплаты
            skills = await list_of_skills[i].get_text() # получаем список навыков
            new_list[i].append(skills) # добавляем список навыков
            company = await list_of_companies[i].get_text() # получаем название компании
            new_list[i].append(company) # добавляем название компании
            #location = await list_of_locations[i].get_text() # получаем расположение
            #new_list[i].append(location) # добавляем расположение
            occupation = await list_of_occupations[summand+1].get_text() # получаем тип занятости
            new_list[i].append(occupation) # добавляем тип занятости

        pool['moi_krug_list'] = new_list

async def fetch_HH_content():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        for i in range(len(pool['headhunter_list'])):
            await session.get(pool['headhunter_list'][i][0])
            company_object = await session.get_element('span[itemprop=name]')
            company_name = await company_object.get_text()
            #location_object = await session.get_element('span[itemprop=jobLocation]')
            #location = await location_object.get_text()
            experience_object = await session.get_element('span[data-qa=vacancy-experience]')
            experience = await experience_object.get_text()
            employment_mode_object = await session.get_element('p[data-qa=vacancy-view-employment-mode]')
            employment_mode = await employment_mode_object.get_text()
            description_object = await session.get_element('div[data-qa=vacancy-description')
            description = await description_object.get_text()

            pool['headhunter_list'][i].append(company_name)
            #pool['headhunter_list'][i].append(location)
            pool['headhunter_list'][i].append(experience)
            pool['headhunter_list'][i].append(employment_mode)
            pool['headhunter_list'][i].append(description)


async def fetch_HH_links():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()
    #url = data['url']
    #keyword = data['keyword']
    async with get_session(service, browser) as session:
        await session.get('https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true')
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
        pool['headhunter_list'] = new_list


def main():
    loop = asyncio.get_event_loop() # создаем событийный цикл
    loop.run_until_complete(fetch_MK_links()) # проводим пока все таски не будут выполнены
    loop = asyncio.get_event_loop()  # создаем событийный цикл
    loop.run_until_complete(fetch_MK_content())


if sys.platform.startswith('win'):
    GECKODRIVER = './geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'

pool = {}

if __name__ == '__main__':
    t0 = time()
    main()
    print("total pool:", pool)
    print('total time SYNCH:', time() - t0 )

    with connect() as session:
        for item in pool['moi_krug_list']:
            link = item[0]
            title = item[1]
            salary = item[2]
            skills = item[3]
            company = item[4]
            work_conditions = item[5]
            description = item[6]
            new_info = MoiKrug(link, title, salary, skills, company, work_conditions, description)
            session.add(new_info)  # добавляем в базу
