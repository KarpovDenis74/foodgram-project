[![foodgram-project]
()
# foodgram-project — [«Продуктовый помощник»](http://github.com/KarpovDenis74/foodgram-project)	
Сайт «Продуктовый помощник»: 
    Сайт рецептов удобно навигированный и структурированный.
    Пользователя выкладывают рецепты блюд. Можно посмотреть рецепты, их описание, добавить в избранное,
    подписаться на авторов рецептов, добавить понравившиеся рецепты в shoplist,
    распечатать список инградиентов, которые входят в рецепты в shoplist и пойти в магазин купить недостающие ингредиенты.

## Подготовка к работе:

1) Скопируйте в рабочую диреторию:
        DockerFile
        docker-compose.yaml
2) Создайте файл .env и заполните его своими значениями. 
        Все нужные переменные и их примерные значения описаны файле .env.template.
3) Запустите процесс сборки и запуска контейнеров:  
        docker-compose up
4) Примените миграции, введите:  
        docker-compose -f docker-compose.yaml exec web python manage.py migrate --noinput
5) Создайте суперпользователя, необходимо ввести:  
        docker-compose -f docker-compose.yaml exec web python manage.py createsuperuser
6) Добавьте  в базу ингредиенты и теги (данные будут взяты из папки data_csv):  
        docker-compose -f docker-compose.yaml exec web python manage load_ingredients
        docker-compose -f docker-compose.yaml exec web python manage.py load_tags
7) Собирите статику:  
        docker-compose -f docker-compose.yaml exec web python manage.py collectstatic

Готово !!! 
   
## Технологии
* [Python](https://www.python.org/) - высокоуровневый язык программирования общего назначения;
* [Django](https://www.djangoproject.com/) - фреймворк для веб-приложений;
* [Django REST framework](https://www.django-rest-framework.org/) - API фреймворк для Django;
* [PostgreSQL](https://www.postgresql.org/) - объектно-реляционная система управления базами данных;
* [Nginx](https://nginx.org/) - HTTP-сервер и обратный прокси-сервер, почтовый прокси-сервер, а также TCP/UDP прокси-сервер общего назначения;
* [Docker](https://www.docker.com/) - ПО для автоматизации развёртывания и управления приложениями в средах с поддержкой контейнеризации;
* [Docker-Compose](https://docs.docker.com/compose/) - инструмент для создания и запуска многоконтейнерных Docker приложений. 
