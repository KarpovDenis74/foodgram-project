[![foodgram-project]
()
# foodgram-project — [«Продуктовый помощник»](http://_____/)	
Сайт «Продуктовый помощник»: 
    Сайт рецептов удобно навигированный и структурированный.
    Пользователя выкладывают рецепты блюд. Можно посмотреть рецепты, их описание, добавить в избранное,
    подписаться на авторов рецептов, добавить понравившиеся рецепты в shoplist,
    распечатать список инградиентов, которые входят в рецепты в shoplist и пойти в магазин купить недостающие ингредиенты.

## Подготовка к работе:

1) Клонируйте репозиторий на локальную машину.  
   git clone /foodgram-project.git
2) Создайте файл .env и заполните его своими значениями. 
   Все нужные переменные и их примерные значения описаны файле .env.template.
3) Запустите процесс сборки и запуска контейнеров:  
        docker-compose up
4) Применить миграции, введите:  
        docker-compose -f docker-compose.yaml exec web python manage.py migrate --noinput
5) Создаем суперпользователя, необходимо ввести:  
        docker-compose -f docker-compose.yaml exec web python manage.py createsuperuser
6) Добавляем в базу ингредиенты и теги:  
        docker-compose -f docker-compose.yaml exec web python manage.py load_ingredients_data
7) Собираем статику:  
        docker-compose -f docker-compose.yaml exec web python manage.py collectstatic
   
   
## Технологии
* [Python](https://www.python.org/) - высокоуровневый язык программирования общего назначения;
* [Django](https://www.djangoproject.com/) - фреймворк для веб-приложений;
* [Django REST framework](https://www.django-rest-framework.org/) - API фреймворк для Django;
* [PostgreSQL](https://www.postgresql.org/) - объектно-реляционная система управления базами данных;
* [Nginx](https://nginx.org/) - HTTP-сервер и обратный прокси-сервер, почтовый прокси-сервер, а также TCP/UDP прокси-сервер общего назначения;
* [Docker](https://www.docker.com/) - ПО для автоматизации развёртывания и управления приложениями в средах с поддержкой контейнеризации;
* [Docker-Compose](https://docs.docker.com/compose/) - инструмент для создания и запуска многоконтейнерных Docker приложений. 
