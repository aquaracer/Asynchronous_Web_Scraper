import asyncio
import pytest
from models1 import HeadHunter_db, engine
from Head_Hunter_backend import HeadHunter
from Base_Jobsite import base_jobsite
from sqlalchemy.sql import select

LINK_1 = 'https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true'
LINK_2 = 'https://ekaterinburg.hh.ru'


@pytest.mark.asyncio
@pytest.mark.parametrize("test_input,expected", [(LINK_1, True), (LINK_2, False)])
async def test_hh_links_negative(test_input,expected):
    test_method = HeadHunter(test_input)
    mytask_1 = asyncio.create_task(test_method.get_links())  # проводим пока все таски не будут выполнены
    await mytask_1
    assert bool(len(test_method.hh_list)) is expected


@pytest.mark.asyncio
async def test_fetch_content():
    test_method = HeadHunter(LINK_1)
    mytask_1 = asyncio.create_task(test_method.get_links())  # проводим пока все таски не будут выполнены
    await mytask_1
    pool = test_method.hh_list
    temp_pool = base_jobsite.pool['headhunter_list']
    mytask_2 = asyncio.create_task(test_method.fetch_content())  # проводим пока все таски не будут выполнены
    await mytask_2
    list_from_base = []
    for i in range(20):
        async with engine.connect() as conn:
            res = await conn.execute(HeadHunter_db.select((HeadHunter_db.c.id == i + 1)))
            ans = await res.fetchall()
            print('ANS', ans)
        if len(ans) == 0:
            break
        arr = list(ans[0][1:6])  # получаем из базы элементы с первого по третий
        print('ARR', arr)
        list_from_base.append(arr)

    print('pool', pool)
    print('list_from_base', list_from_base)
    for i in len(pool):
        if pool[i] != list_from_base[i]:
            print('Pool[i]', pool[i])
            print('list_from_base[i]', list_from_base[i])
            flag = 1

    print('flag', flag)
    if pool == list_from_base:
        answer = True
    else:
        answer = False

    assert answer == False

