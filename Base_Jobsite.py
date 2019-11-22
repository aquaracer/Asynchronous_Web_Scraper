import asyncio
import sys
from time import time
from arsenic import get_session, keys, browsers, services
from sqlalchemy.schema import CreateTable, DropTable
from sqlalchemy_aio import ASYNCIO_STRATEGY


class base_jobsite():

    if sys.platform.startswith('win'):
        GECKODRIVER = './geckodriver.exe'
    else:
        GECKODRIVER = './geckodriver'

    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()

    async def get_links(self):
        pass

    async def get_content(self):
        pass

    pool ={}