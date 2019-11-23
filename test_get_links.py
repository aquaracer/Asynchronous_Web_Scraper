import asyncio
import pytest

from Head_Hunter_backend import HeadHunter


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def test_Get_hh_links(event_loop):
    test_method = HeadHunter()
    event_loop.run_until_complete(test_method.get_links())
    assert len(test_method.hh_list) > 0
