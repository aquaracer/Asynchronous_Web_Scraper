import sys
from arsenic import browsers, services
from abc import ABCMeta, abstractmethod


class base_jobsite():
    """  Абстрактный базовый класс для классов сайтов с вакансиями.

    Назначение: определить набор методов, которые должны быть созданы в любых дочерних классах

    """

    __metaclass__ = ABCMeta

    if sys.platform.startswith('win'):
        GECKODRIVER = './geckodriver.exe'
    else:
        GECKODRIVER = './geckodriver'

    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox(firefoxOptions={'args': ['-headless']})

    @abstractmethod
    async def get_links(self):
        """Корутина, получающая ссылки на страницы с вакансиями"""
        pass

    @abstractmethod
    async def get_content(self):
        """Корутина, получающая данные с страницы с вакансиями"""
        pass
