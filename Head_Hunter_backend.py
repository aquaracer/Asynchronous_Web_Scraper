from Base_Jobsite import base_jobsite
from arsenic import get_session
from models1 import HeadHunter_db, engine
from sqlalchemy.schema import CreateTable
import asyncio
import random


# START_URL = 'https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true'
# 'https://ekaterinburg.hh.ru'


class HeadHunter(base_jobsite):
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)

    def __init__(self, START_URL):
        self.START_URL = START_URL

    async def get_links(self, queue=queue, limit=None):
        """Метод получает на вход очередь.
        Назначение: собрать данные с первой страницы результатов поиска по заданному ключевому слову и передать их
        через очередь для дальнейшей обработки в метод fetch_content.
        Сначала метод загружает по ссылке(self.START_URL) страницу с результатами поиска по заданному ключевому
        слову. Затем асинхронно создает следующие списки: ссылки на вакансии, названиz вакансий, зарплаты,
        требования к кандидату. Затем в цикле создаем элементы очереди, состоящие  из ссылки на вакансию, названия
        вакансии, зарплаты и требований.  Как только элемент создан - вносим его в очередь для передачи
        в метод fetch_content, который собирает информацию по заданной ссылке и сохраняет их в базе
        данных. По завершению цикла - добавляем None в качестве последнего элемента очередь. Получив элемент None
        из очереди, метод fetch_content прекращает работу."""


        async with get_session(self.service, self.browser) as session:
            await session.get(self.START_URL)  # переходим по ссылке
            list_of_titles = await session.get_elements(
                'a[data-qa=vacancy-serp__vacancy-title]')  # собираем названия вакансий в список
            list_of_compensations = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy-compensation]')  # собираем зарплаты в список
            list_of_responsibilities = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy_snippet_responsibility]')  # собираем краткие описания вакансий в список
            list_of_requirements = await session.get_elements(
                'div[data-qa=vacancy-serp__vacancy_snippet_requirement]')  # собираем требования к кандидату в список
            new_list = []
            rows_per_page = len(list_of_titles)
            if limit:
                rows_per_page = limit
            for i in range(rows_per_page):  # создаем объекты для передачи в очередь
                # как только первый объект появится в очереди - он будет передан в метод fetch_content
                # для сбора содержания страницы и сохранения его в базе данных
                link = await list_of_titles[i].get_attribute('href')
                new_list.append([link])  # добавляем ссылку на вакансию в список
                title = await list_of_titles[i].get_text()
                new_list[i].append(title)  # добавляем название вакансии по ссылке в список
                compensation = await list_of_compensations[i].get_text()
                new_list[i].append(compensation)  # добавляем зарплаты по вакансии по ссылке в список
                responsibility = await list_of_responsibilities[i].get_text()
                new_list[i].append(responsibility)  # добавляем краткое описание вакансии по ссылке в список
                requirements = await list_of_requirements[i].get_text()
                new_list[i].append(requirements)  # добавляем требования по вакансии по ссылке в список
                await queue.put(new_list[i])  # добавляем текущий список из ссылки, названия вакансии, зарплаты,
                # краткого описания и требований для передачи в функцию fetch_content,
                # которая откроет ссылку, соберет необходимую информацию на странице и
                # сохранит в базе данных
            await queue.put(None)  # после завершения цикла добавляем обьект None в конец очереди


    async def fetch_content(self, queue=queue):
        """Метод получает на вход очередь c данными о вакансиях.
        Назначение: асинхронно собрать информацию о вакансиях и записать ее в базу данных.
        Сначала метод создает таблицу в базе данных для записи информации на текущую дату. Далее запускает
        бесконечный цикл, в котором ожидает получения элемента(списка с данными) из очереди. Получив элемент,
        загружает по полученной из элемента ссылке страницу с информацией о вакансии. Со страницы асинхронно получаем
        название компании, требуемый опыт кандидата, тип занятости и полное описание вакансии. Полученные данные
        записываем в базу. Условием выхода из цикла является получение элемента None из очереди.
        Работа данного метода связана с работой метода get_links. Получив ссылку со страницы результатов поиска, метод
        get_links передает ссылку в метод fetch_content. Метод fetch_content начинает загразку страницы с вакансией и
        сбор информации. Не дождавшись завершения процесса и получив новый элемент из очереди, метод fetch_content
        открывает новую страницу по ссылке и начинает сбор данных с нее. Так продолжается пока в очереди есть элементы.
        Таким образом одновременно идет сбор информации со всех ссылок из списка, что позволяет в разу сократить время
        выполнения задачи по сбору данных."""
        await engine.execute(
            CreateTable(HeadHunter_db))  # создаем таблицу для сохранения данных о вакансии на текущую дату
        while True:
            # wait for an item from the producer
            item = await queue.get()
            if item is None:  # если получен элемент None значит очередь закончилась
                # the producer emits None to indicate that it is done
                break
            async with get_session(self.service, self.browser) as web_session:
                await web_session.get(item[0])  # загражаем страницу по ссылке из списка и получаем объекты на странице
                company_object = await web_session.get_element('span[itemprop=name]')
                company = await company_object.get_text()  # получаем название компании по текущей ссылке
                experience_object = await web_session.get_element('span[data-qa=vacancy-experience]')
                experience = await experience_object.get_text()  # получаем требуемый опыт кандидата по текущей ссылке
                employment_mode_object = await web_session.get_element('p[data-qa=vacancy-view-employment-mode]')
                employment_mode = await employment_mode_object.get_text()  # получаем тип занятости по текущей ссылке
                description_object = await web_session.get_element('div[data-qa=vacancy-description')
                description = await description_object.get_text()  # получаем полное описание вакансии по текущей ссылке
                async with engine.connect() as conn:  # записываем данные в базу
                    async with conn.begin() as trans:
                        await conn.execute(HeadHunter_db.insert().values(link=item[0], title=item[1], salary=item[2],
                                                                         responsibilites_short=item[3],
                                                                         requirements_short=item[4],
                                                                         company=company, experience=experience,
                                                                         employment_mode=employment_mode,
                                                                         description=description))
            await asyncio.sleep(random.random())
