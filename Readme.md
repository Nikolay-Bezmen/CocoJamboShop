# CocoJamboShop Backend

## Описание проекта

CocoJamboShop — это онлайн-платформа для продажи товаров, позволяющая пользователям регистрироваться, просматривать товары, добавлять их в корзину и оформлять заказы. Администраторы могут управлять товарами и заказами через админ-панель.

## Стек используемых технологий

- **Язык программирования:** Python 3.9
- **Фреймворк:** Django + Django REST Framework
- **База данных:** SQLite (на этапе разработки), возможно переход на PostgreSQL
- **Докеризация:** Docker, Docker Compose
- **Система управления версиями:** Git
- **Виртуальное окружение:** pip, venv
- **Контейнеризация:** Docker

## Роли пользователей и описание их действий в системе

1. **Покупатель:**
   - Регистрация и авторизация.
   - Просмотр каталога товаров.
   - Поиск товаров по категориям.
   - Добавление товаров в корзину.
   - Оформление заказа.
   
2. **Администратор:**
   - Управление товарами (добавление, изменение, удаление).
   - Управление заказами (обработка, подтверждение, отмена).

### Диаграмма вариантов использования

![Диаграмма вариантов использования](ссылка-на-картинку-диаграммы.png)

## Схема БД - ER диаграмма

ER диаграмма отображает полную структуру базы данных, включая связи между сущностями, такими как **Пользователи**, **Товары**, **Заказы**.

![ER-диаграмма](https://drive.google.com/file/d/1_DfwZePcwFNyMNtgXQtb2dxwaJdmBlL2/view?usp=drive_link) 

## API

| HTTP метод | Эндпоинт             | Описание                  |
|------------|----------------------|---------------------------|
| GET        | /api/products/        | Получить список товаров   |
| GET        | /api/products/{id}/   | Получить товар по ID      |
| POST       | /api/orders/          | Создать новый заказ       |
| GET        | /api/orders/{id}/     | Получить детали заказа    |
| PUT        | /api/orders/{id}/     | Обновить информацию о заказе |
| DELETE     | /api/orders/{id}/     | Удалить заказ             |
| POST       | /api/auth/login/      | Вход пользователя         |
| POST       | /api/auth/register/   | Регистрация пользователя  |


# CocoJamboShop Frontend

## Описание проекта

CocoJamboShop — это клиентская часть онлайн-магазина, обеспечивающая удобный интерфейс для покупателей. Пользователи могут просматривать каталог товаров, добавлять их в корзину и оформлять заказы. Администраторы могут использовать административную панель для управления товарами и заказами.

## Стек используемых технологий

- **Язык программирования:** JavaScript
- **Фреймворк:** React.js
- **Менеджер состояния:** Redux
- **Стилизация:** CSS (или SCSS), Material-UI
- **Сборка проекта:** Webpack
- **Контейнеризация:** Docker

## Ссылка на прототипы страниц

[Ссылка на Figma/другие прототипы страниц](https://www.figma.com/design/p1rT2000WCQTpeaHCHB5m1/COCO-SHOP-Apple-technic?node-id=0-1&t=mymV8TJtwiGBPBIF-1)

## Ссылка на API сервера

Frontend взаимодействует с backend API для получения данных о товарах, заказах и пользователях.

# Проект на Django с использованием Swagger для документации

## Установка и настройка
1. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

2. Выполните миграции:
    ```bash
    python manage.py migrate
    ```

3. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

## Доступ к документации

После запуска сервера, документация API будет доступна по следующим URL:

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **JSON схема**: [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json)
- **YAML схема**: [http://localhost:8000/swagger.yaml](http://localhost:8000/swagger.yaml)

## Использование с Postman
1. Откройте Postman.
2. Создайте новый запрос.
3. Установите метод **POST** и URL [http://localhost:8000/api/token/](http://localhost:8000/api/token/).
4. Перейдите на вкладку Body, выберите `raw`, установите формат в `JSON` и добавьте:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
5. Отправьте запрос и получите токен.
6. Используйте полученный токен для доступа к защищённым маршрутам, добавляя его в заголовок `Authorization` следующих запросов:
    ```plaintext
    Authorization: Bearer your_access_token
    ```

## Поддержка
Если у вас возникли вопросы или проблемы, пожалуйста, свяжитесь с нашей командой поддержки.
