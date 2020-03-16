from base_jobsite import base_jobsite
from arsenic import get_session
from models1 import MoiKrug_db, engine
from sqlalchemy.schema import CreateTable
import asyncio


class MyCircle(base_jobsite):
    """Класс MyCircle.
    Конструктор принимает ссылку на страницу с результатами поиска по заданному ключевому
    слову по сайту moikrug.ru

    """
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)

    def __init__(self, START_URL):
        self.START_URL = START_URL

    async def get_links(self):
        """Корутина получения ссылок.

        Корутина получает на вход очередь.
        Назначение: собрать данные с первой страницы результатов поиска по заданному ключевому слову и передать их
        через очередь для дальнейшей обработки в корутину fetch_content.
        Сначала метод загружает по ссылке(self.START_URL) страницу с результатами поиска по заданному ключевому
        слову. Затем асинхронно создает следующие списки: ссылки на вакансии, названия вакансий, зарплаты,
        требования к кандидату, названия компаний, типы занятости. Затем в цикле создаем элементы очереди, состоящие
        из ссылки на вакансию, названия вакансии, зарплаты, требований к кандидату, названия компнании, типа занятости.
        Как только элемент создан - вносим его в очередь для передачи в метод fetch_content, который собирает
        информацию по заданной ссылке и сохраняет ее в базе данных. По завершению цикла - добавляем None в качестве
        последнего элемента в очередь. Получив элемент None из очереди, метод fetch_content прекращает работу.

        """
        async with get_session(self.service, self.browser) as session:
            await session.get(self.START_URL)
            list_of_links = await session.get_elements('a[class=job_icon]')  # создаем список ссылок на вакансии
            list_of_titles = await session.get_elements('div[class=title]')  # создаем список названий вакансий
            filtred_list_of_titles = []
            for item in list_of_titles:
                title = await item.get_attribute('title')
                if title != None:
                    filtred_list_of_titles.append(title)  # получаем отфильтрованный список названий вакансий
            banner_vacancy = await session.get_element(
                'div[class=vacancy_banner]')  # проверяем есть ли рекламная вакансия в баннере. если есть - в итоговый
                                              # список типов занятости заносим элемент, начиная с первого
            banner_content = await banner_vacancy.get_text()
            if banner_content == None:
                summand = 0
            else:
                summand = 1
            list_of_compensations = await session.get_elements('div[class=count')  # создаем список зарплат
            list_of_skills = await session.get_elements('div[class=skills]')  # создаем список требований
            list_of_companies = await session.get_elements(
                'span[class=company_name]')  # создаем список названий компаний
            list_of_occupations = await session.get_elements('span[class=occupation]')  # создаем список типов занятости
            queue_item = []  # элемент очереди в виде пустого списка
            rows_per_page = len(list_of_links)
            for i in range(rows_per_page):  # в цикле создаем элементы и передаем их через очередь
                                            # в метод fetch_content
                link = await list_of_links[i].get_attribute('href')  # получаем ссылку
                link = f'https://moikrug.ru{link}'
                queue_item.append([link])  # добавляем ссылку элемент очереди
                queue_item[i].append(filtred_list_of_titles[i])  # добавляем название вакансии в элемент очереди
                compensation = await list_of_compensations[i].get_text()  # получаем размер зарплаты в элемент очереди
                queue_item[i].append(compensation)  # добавляем размер зарплаты в элемент очереди
                skills = await list_of_skills[i].get_text()
                queue_item[i].append(skills)  # добавляем список навыков в элемент очереди
                company = await list_of_companies[i].get_text()
                queue_item[i].append(company)  # добавляем название компании в элемент очереди
                occupation = await list_of_occupations[i].get_text()
                queue_item[i].append(occupation)  # добавляем тип занятости в элемент очереди
                await self.queue.put(
                    queue_item[i])  # добавляем в виде списка с данными элемент в очередь для дальнейшей
                                    # обработки
            await self.queue.put(None)  # после завершения цикла добавляем обьект None в конец очереди, чтобы обозначить
                                        # прекращение обработки данных

    async def fetch_content(self):
        """Корутина сбора данных со страницы вакансии.

        Корутина получает на вход очередь c данными о вакансиях.
        Назначение: асинхронно собрать информацию о вакансиях и записать ее в базу данных.
        Сначала метод создает таблицу в базе данных для записи информации на текущую дату. Далее запускает
        бесконечный цикл, в котором ожидает получения элемента(списка с данными) из очереди. Получив элемент,
        загружает по полученной из элемента ссылке страницу с информацией о вакансии. Со страницы асинхронно
        получает полное описание вакансии. Полученные данные(ссылка на вакансию, название вакансии, зарплата,
        требования к кандидату, название компнании, тип занятости, полное описание вакансии)записываем в базу.
        Условием выхода из цикла является получение элемента None из очереди.
        Работа данного метода связана с работой метода get_links. Получив ссылку со страницы результатов поиска, метод
        get_links передает ссылку в метод fetch_content. Метод fetch_content начинает загрузку страницы с вакансией и
        сбор информации. Не дождавшись завершения процесса и получив новый элемент из очереди, метод fetch_content
        открывает новую страницу по ссылке и начинает сбор данных с нее. Так продолжается пока в очереди есть элементы.
        Таким образом одновременно идет сбор информации со всех ссылок из списка, что позволяет в разы сократить время
        выполнения задачи по сбору данных.

        """
        await engine.execute(CreateTable(MoiKrug_db))  # создаем таблицу для хранения данных о вакансии на текущую дату
        while True:
            item = await self.queue.get()  # ждем пока появится новый элемент в очереди
            if item is None:  # Элемент None означает конец очереди
                break
            async with get_session(self.service, self.browser) as web_session:
                await web_session.get(item[0])  # загружаем страницу вакансии
                description_object = await web_session.get_element('div[class=vacancy_description]')
                description = await description_object.get_text()  # получаем описание вакансии
                async with engine.connect() as conn:
                    async with conn.begin() as trans:
                        await conn.execute(MoiKrug_db.insert().values(link=item[0],  # записываем данные в базу
                                                                      title=item[1], salary=item[2], skills=item[3],
                                                                      company=item[4], occupation=item[5],
                                                                      description=description))

