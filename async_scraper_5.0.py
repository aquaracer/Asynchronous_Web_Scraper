import asyncio
from time import time
from arsenic import get_session, keys, browsers, services
from Head_Hunter_backend import HeadHunter
from MyCircle_backend import MyCircle
from Base_Jobsite import base_jobsite


async def start_method(method_gets_links, method_gets_content):
    mytask_1 = asyncio.create_task(method_gets_links)  # проводим пока все таски не будут выполнены
    await mytask_1
    mytask_2 = asyncio.create_task(method_gets_content)
    await mytask_2


async def run_1(data_list):
    tasks = []
    async with get_session(base_jobsite.service, base_jobsite.browser) as session:
        for data in data_list:
            task = asyncio.ensure_future(start_method(data[0],data[1]))  # назначаем таск в виде метода fetch
            tasks.append(task) # добавляем таск в список назначенных тасков
        responses = asyncio.gather(*tasks) # создаем список тасков для выполнения
        await responses
    return responses

HeadHunter_data = HeadHunter()
MyCircle_data = MyCircle()

data_list=[[HeadHunter_data.get_links(),HeadHunter_data.fetch_content()],
           [MyCircle_data.get_links(), MyCircle_data.fetch_content()]]


if __name__ == '__main__':
    t0 = time()
    asyncio.run(run_1(data_list))
    print("total pool:", base_jobsite.pool)
    print('total time SYNCH:', time() - t0)





