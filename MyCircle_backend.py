from Base_Jobsite import base_jobsite
from arsenic import get_session
from models1 import MoiKrug_db, engine
from sqlalchemy.schema import CreateTable


class MyCircle(base_jobsite):

    def __init__(self, START_URL):
        self.START_URL = START_URL

    async def get_links(self):
        async with get_session(self.service, self.browser) as session:
            await session.get(START_URL)
            list_of_links = await session.get_elements('a[class=job_icon]')  # получаем список линков
            list_of_titles = await session.get_elements('div[class=title]')  # 'a[class=job_icon]'
            filtred_list_of_titles = []
            for item in list_of_titles:
                title = await item.get_attribute('title')
                if title != None:
                    filtred_list_of_titles.append(title)  # получаем отфильтрованный список названий вакансий
            banner_vacancy = await session.get_element(
                'div[class=vacancy_banner]')  # проверяем есть ли рекламная вакансия в баннере. если есть - в итоговый список типов занятости заносим элемент, начиная с первого
            banner_content = await banner_vacancy.get_text()
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
            base_jobsite.pool['moi_krug_list'] = new_list


    async def fetch_content(self):
        await engine.execute(CreateTable(MoiKrug_db))
        async with get_session(self.service, self.browser) as web_session:
            for i in range(len(base_jobsite.pool['moi_krug_list'])):
                await web_session.get(base_jobsite.pool['moi_krug_list'][i][0])
                description_object = await web_session.get_element('div[class=vacancy_description]')
                description = await description_object.get_text()
                async with engine.connect() as conn:
                    async with conn.begin() as trans:
                        await conn.execute(MoiKrug_db.insert().values(link=base_jobsite.pool['moi_krug_list'][i][0],
                              title=base_jobsite.pool['moi_krug_list'][i][1], salary=base_jobsite.pool['moi_krug_list'][i][2],
                              skills=base_jobsite.pool['moi_krug_list'][i][3], company=base_jobsite.pool['moi_krug_list'][i][4],
                              occupation=base_jobsite.pool['moi_krug_list'][i][5], description=description))