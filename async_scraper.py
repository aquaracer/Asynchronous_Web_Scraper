import asyncio
import sys

from arsenic import get_session, keys, browsers, services

if sys.platform.startswith('win'):
    GECKODRIVER = './geckodriver.exe'
else:
    GECKODRIVER = './geckodriver'


async def pars_url():
    service = services.Geckodriver(binary=GECKODRIVER)
    browser = browsers.Firefox()

    async with get_session(service, browser) as session:
        await session.get("https://moikrug.ru/vacancies?q=3d+s+max&sort=date&currency=rur&remote=1") # открыываем странице с запросом на вакансию
        list_of_url = await session.get_elements('a[class=job_icon]')  # получаем массив элемнтов с именем класса 'job_icon'
        final_list_of_urls = []
        for item in list_of_url:
            element_2 = item.get_text()
            print('type item', type(item))  # type item <class 'arsenic.session.Element'>
            print('element_2', element_2) #  element_2 <coroutine object Element.get_text at 0x10b473cc8>
            print('type element_2', type(element_2)) # type element_2 <class 'coroutine'>
            final_list_of_urls.append(element_2)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pars_url())


if __name__ == '__main__':
    main()
