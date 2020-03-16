import asyncio
from head_hunter_backend import HeadHunter
from mycircle_backend import MyCircle

LINKS = {'MyCirle': "https://moikrug.ru/vacancies?q=3ds+max&currency=rur&with_salary=1",
         'HeadHunter': "https://ekaterinburg.hh.ru/search/vacancy?area=1261&clusters=true&enable_snippets=true&text=python&only_with_salary=true&from=cluster_compensation&showClusters=true"}

HHunter = HeadHunter(LINKS['HeadHunter'])
MCircle = MyCircle(LINKS['MyCirle'])

loop = asyncio.get_event_loop()
HHunter_get_links = HHunter.get_links()
HHunter_fetch_content = HHunter.fetch_content()
MCircle_get_links = MCircle.get_links()
MCircle_fetch_content = MCircle.fetch_content()

loop.run_until_complete(
    asyncio.gather(MCircle_get_links, MCircle_fetch_content, HHunter_get_links, HHunter_fetch_content))
loop.close()
