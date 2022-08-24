Портал игровых новостей сделан на основе новостного сайта с тематикой игр blizzard - glasscannon.ru<br>

<b>stack</b>:<br>
  Django, DRF, Docker-compose, PostgreSql, Celery, Redis, DRF, CSS, HTML, JS
 
<b>Конфигурация проекта:</b><br>
  Все личные данные от почты, Редис, берутся из виртуального окружения. Для полного функционирования проекта необходимо указать свои данные либо в settings.py, либо также вынести в .env<br>

<b>Запуск проекта</b><br>
  <b> Стандартный, без докер: </b><br>
    1) python manage.py shell (вставить текст комманд из файла комманды.txt для наполнения тестовыми данными БД)<br>
    2) python manage.py runserver<br>
    
  <b>Запуск проекта с помощью docker-compose</b><br>

  1)docker compose build (создаем/импортируем образы, формируем сервисы)<br>
  2)docker compose up (пред запуск проекта)<br>
  <u>в отдельной консоли:</u><br>
  3)docker exec -i db_pg pg_restore -U postgres --verbose --clean --no-acl --no-owner -h localhost -d gamenews db.backup<br> (установка дампа начальной БД).<br>
  4)docker compose down - останавливаем контенеры (для применения изменений в БД)<br>
  5)docker compose up - все последующие запуски проекта<br>

    Для запуска задач по расписанию:<br>
      2)docker compose run web celery -A gamenews_proj worker -l info -P eventlet  (2-м окном терминала)<br>
      3)docker compose run web celery -A gamenews_proj beat (3м окном терминала)<br>

<b>Функциональность проекта</b>:

    -API (на основной странице приведено меню из возможных ссылок - http://127.0.0.1:8000/api/submit-data/):
      документация к API - http://127.0.0.1:8000/api/swagger/ или http://127.0.0.1:8000/api/redoc/
      Авторизация - http://127.0.0.1:8000/api/auth/login/
      CRUD для сущностей - POST (новости), CategoryPost (m2m связь категорий и новостей), CategoryUser (m2m - подписчики  к категориям)
      Пагинация
      Фильтрация
      Прокинуты права по принципу изменять данные может пользователь - создатель, удалять администратор, 
      проссматривать - любой пользователь
    -Портал игровых новостей:
      *CRUD для размещения новостей, прокинуты соответсвующие права.
      *ЛК, где пользователь может:
        1) установить/сбросить свой аватар, 
        2) изменить личные данные в т.ч. логин и пароль.
        3) получить права автора и отказаться от  них
        4) модерировать комментарии к своим статьям (в работе)
      *фильтрация новостей по категориям, поиск по ключевым словам, а также пагинация с учетом поиска и фильтрации.
      *Реализована возможность авторизованному пользователю подписаться на статью (на все категории этой статьи).
        Подписчикам по категориям на которые они подписаны мгновенно приходит сообщение на почту о появлении новой новости по сигналу.
        Также помощью CELERY осуществляется еженедельная отправка сообщений по всем новым статья за неделю.

  В работе:
    - Добавить функционал для добавления пользователями комментариев к статьям и модеррировании этих комментариев администрацией
    
