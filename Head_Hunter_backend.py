from Base_Jobsite import base_jobsite
from arsenic import get_session
from models1 import HeadHunter_db, engine
from sqlalchemy.schema import CreateTable, DropTable
import asyncio
import random

#START_URL = 'https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true'
                #'https://ekaterinburg.hh.ru'


class HeadHunter(base_jobsite):

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    HeadHunter_list = None

    def __init__(self, START_URL):
        self.START_URL = START_URL

<<<<<<< HEAD

    async def get_links(self, queue=queue, limit = None):
=======
    async def get_links(self, queue):
>>>>>>> 7d2de028f3039bda712b93b3f188f4ee59be9385
        await engine.execute(CreateTable(HeadHunter_db)) # создаем таблицу
        async with get_session(self.service, self.browser) as session:
            await session.get(self.START_URL)   # собираем 4 массива чтобы сделать 1 общий массив
            list_of_titles = await session.get_elements('a[data-qa=vacancy-serp__vacancy-title]')  # 'a[class=job_icon]'
            print("LIST_OF_TITLES", list_of_titles)
            list_of_compensations = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy-compensation]')  # 'a[class=job_icon]'
            list_of_responsibilities = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy_snippet_responsibility]')
            list_of_requirements = await session.get_elements('div[data-qa=vacancy-serp__vacancy_snippet_requirement]')
            new_list = []
            number = len(list_of_titles)
            if limit :
                number = limit
            for i in range(number):
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
                await queue.put(new_list[i])
            await queue.put(None)
<<<<<<< HEAD
            self.HeadHunter_list = list_of_titles


    async def fetch_content(self, queue=queue):
=======
            #base_jobsite.pool['headhunter_list'] = new_list
            #self.hh_list = new_list

    async def fetch_content(self, queue):
>>>>>>> 7d2de028f3039bda712b93b3f188f4ee59be9385
        while True:
            # wait for an item from the producer
            item = await queue.get()
            if item is None:
                # the producer emits None to indicate that it is done
                break
<<<<<<< HEAD
=======

>>>>>>> 7d2de028f3039bda712b93b3f188f4ee59be9385
            async with get_session(self.service, self.browser) as web_session:
                await web_session.get(item[0])  # загражаем страницу по линку из списка и получаем объекты на странице
                company_object = await web_session.get_element('span[itemprop=name]')
                company = await company_object.get_text()
                experience_object = await web_session.get_element('span[data-qa=vacancy-experience]')
                experience = await experience_object.get_text()
                employment_mode_object = await web_session.get_element('p[data-qa=vacancy-view-employment-mode]')
                employment_mode = await employment_mode_object.get_text()
                description_object = await web_session.get_element('div[data-qa=vacancy-description')
                description = await description_object.get_text()
                async with engine.connect() as conn:       # записываем данные в базу
                    async with conn.begin() as trans:
                        await conn.execute(HeadHunter_db.insert().values(link=item[0],
                        title=item[1], salary=item[2], responsibilites_short=item[3], requirements_short=item[4],
                        company=company, experience=experience, employment_mode=employment_mode, description=description))
            await asyncio.sleep(random.random())