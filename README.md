# TestTask
При запуске проекта: 

http://127.0.0.1:8000/api/clients/create/ - создание нового пользователя
http://127.0.0.1:8000/auth/jwt/create/ - авторизация пользователя и создание токена для него
http://127.0.0.1:8000/api/list - получение спика всех пользователей *
    (фильрация по полям: 'first_name', 'last_name', 'gender', 'distance' (в километрах)
http://127.0.0.1:8000/api/clients/(id пользовтеля)/match/ - функция реакции на профиль пользователя, при взаимной реакции
отправляются письма на почту *
 
*-работают только для авторизованного пользователя