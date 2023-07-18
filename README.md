Для создания образа docker надо в папке с проектом ввести команду:
docker compose up -d

В контейнере создается база данных и таблица sql скриптом, также устанавливаются все зависимости из requirements.txt

Реализовано 5 методов: get_one, get_all, post, patch, delete

В рамках контейнера api доступно по url:
http://0.0.0.0:8010/api/ - для методов get_all и post
http://0.0.0.0:8010/api/{id} - для методов get_one, patch, delete
