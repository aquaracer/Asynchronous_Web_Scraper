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
        await session.get("https://moikrug.ru/vacancies?q=3d+s+max&sort=date&currency=rur&remote=1")
        list_of_url = await session.get_elements('a[class=job_icon]')  # // await
        for item in list_of_url:
            element_2 = item.get_text()
            print('dir(element_2)', dir(element_2))
            print('type item', type(item))
            print('element_2', element_2)
            print('type element_2', type(element_2))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pars_url())


if __name__ == '__main__':
    main()
