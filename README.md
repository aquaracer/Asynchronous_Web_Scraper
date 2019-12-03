Разработать парсер для сбора информации о вакансиях с сайтов по поиску работы.  

 
 Производится сбор следующих данных:
- название вакансии
- краткое описание вакансии
- полное описание вакансии
- название компании
- зарплата
- требования
- опыт работы

### База данных.
В качестве ORM использовать sqlalchemy. В качестве СУБД использовать PostgresSQL.

### Асинхронность
Реализовать возможность асинхронного сбора и асинхронного сохранения данных с нескольких сайтов. Использовать библиотеку Asyncio. Для сбора данных с сайтов использовать библиотеки Selenuim + Arsenic.

### Тестирование
Провести тестирование сервиса посредством Pytest.