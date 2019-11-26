import asyncio
from time import time
from arsenic import get_session, keys, browsers, services
from Head_Hunter_backend import HeadHunter
from MyCircle_backend import MyCircle
from Base_Jobsite import base_jobsite


LINKS = {'MyCirle': "https://moikrug.ru/vacancies?q=3ds+max&currency=rur&with_salary=1",
         'HeadHunter': "https://ekaterinburg.hh.ru/search/vacancy?order_by=salary_desc&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true" }


HHunter = HeadHunter(LINKS['HeadHunter'])
MCircle = MyCircle(LINKS['MyCirle'])

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
HHunter_get_links = HHunter.get_links(queue)
HHunter_fetch_content = HHunter.fetch_content(queue)
MCircle_get_links = MCircle.get_links(queue)
MCircle_fetch_content = MCircle.fetch_content(queue)

loop.run_until_complete(asyncio.gather(MCircle_get_links, MCircle_fetch_content, HHunter_get_links, HHunter_fetch_content))
loop.close()
