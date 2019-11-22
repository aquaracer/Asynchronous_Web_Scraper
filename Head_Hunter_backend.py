from Base_Jobsite import base_jobsite
import asyncio
import sys
from arsenic import get_session, keys, browsers, services
from models1 import HeadHunter_db, MoiKrug_db, engine
from sqlalchemy.schema import CreateTable, DropTable
from sqlalchemy_aio import ASYNCIO_STRATEGY


class HeadHunter(base_jobsite):

    async def get_links(self):
        #base = base_jobsite()
        #service, browser= base.setup_browser()
        async with get_session(base_jobsite.service, base_jobsite.browser) as session:
            await session.get(
                'https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true')
            list_of_titles = await session.get_elements('a[data-qa=vacancy-serp__vacancy-title]')  # 'a[class=job_icon]'
            list_of_compensations = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy-compensation]')  # 'a[class=job_icon]'
            list_of_responsibilities = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy_snippet_responsibility]')
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
            base_jobsite.pool['headhunter_list'] = new_list


    async def fetch_content(self):
        #base = base_jobsite()
        #service, browser = base.setup_browser()
        await engine.execute(CreateTable(HeadHunter_db))
        async with get_session(base_jobsite.service, base_jobsite.browser) as web_session:
            for i in range(len(base_jobsite.pool['headhunter_list'])):  # идем поэлементно по списку линков
                await web_session.get(base_jobsite.pool['headhunter_list'][i][0])  # загражаем линк из списка
                company_object = await web_session.get_element('span[itemprop=name]')
                company = await company_object.get_text()
                experience_object = await web_session.get_element('span[data-qa=vacancy-experience]')
                experience = await experience_object.get_text()
                employment_mode_object = await web_session.get_element('p[data-qa=vacancy-view-employment-mode]')
                employment_mode = await employment_mode_object.get_text()
                description_object = await web_session.get_element('div[data-qa=vacancy-description')
                description = await description_object.get_text()
                async with engine.connect() as conn:
                    async with conn.begin() as trans:
                        await conn.execute(HeadHunter_db.insert().values(link=base_jobsite.pool['headhunter_list'][i][0],
                        title=base_jobsite.pool['headhunter_list'][i][1], salary=base_jobsite.pool['headhunter_list'][i][2],
                        responsibilites_short=base_jobsite.pool['headhunter_list'][i][3], requirements_short=base_jobsite.pool['headhunter_list'][i][4],
                        company=company, experience=experience, employment_mode=employment_mode, description=description))