import sys
from arsenic import browsers, services



class base_jobsite():

    if sys.platform.startswith('win'):
        GECKODRIVER = './geckodriver.exe'
    else:
        GECKODRIVER = './geckodriver'

    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()

    pool = {}

    async def get_links(self):
        pass

    async def get_content(self):
        pass

