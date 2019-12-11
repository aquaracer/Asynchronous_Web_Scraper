import asyncio
import pytest
from models1 import HeadHunter_db, engine
from Head_Hunter_backend import HeadHunter
from Base_Jobsite import base_jobsite
from sqlalchemy.sql import select
from sqlalchemy.schema import DropTable

LINK_1 = 'https://ekaterinburg.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=java&enable_snippets=true&only_with_salary=true'
LINK_2 = 'https://ekaterinburg.hh.ru'


@pytest.fixture
def loop():
    return asyncio.get_event_loop()


@pytest.fixture
def queue_factory():
    def wrapper(loop):
        return asyncio.Queue(loop=loop)
    return wrapper


@pytest.mark.asyncio
@pytest.mark.parametrize("test_input,expected_entries", [(LINK_1, 2), (LINK_2, 0)])
async def test_fetch_content(test_input, expected_entries, queue_factory, loop):
    queue = queue_factory(loop)
    limit = 2
    test_method = HeadHunter(test_input)
    mytask_1 = asyncio.create_task(test_method.get_links(queue, limit))  # проводим пока все таски не будут выполнены
    await mytask_1
    mytask_2 = asyncio.create_task(test_method.fetch_content(queue))  # проводим пока все таски не будут выполнены
    await mytask_2
    async with engine.connect() as conn:
        data_object = await conn.execute(HeadHunter_db.select())
        current_data = await data_object.fetchall()
    actual_entries = len(current_data)
    await engine.execute(DropTable(HeadHunter_db))
    assert expected_entries == actual_entries


@pytest.mark.asyncio
@pytest.mark.parametrize("test_input,expected", [(LINK_1, True), (LINK_2, False)])
async def test_hh_links(test_input, expected, queue_factory, loop):
      queue = queue_factory(loop)
      test_method = HeadHunter(test_input)
      #expected = False
      mytask_1 = asyncio.create_task(test_method.get_links(queue))  # проводим пока все таски не будут выполнены
      await mytask_1
      await engine.execute(DropTable(HeadHunter_db))
      assert bool(len(test_method.HeadHunter_list)) is expected
