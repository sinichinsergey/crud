# REST API сервер «Адресная книга»

## Описание
REST API сервер для управления адресной книгой, включающий в себя пользователей, их телефоны и электронные адреса. Реализован полноценный CRUD для каждой сущности.

## Задачи
- Создать базу данных на РСУБД PostgreSQL согласно предоставленной структуре.
- Написать скрипт для автоматического заполнения данных структуры случайными значениями.
- Реализовать CRUD операции для каждой сущности:
  - Получение данных - HTTP POST
  - Создание сущностей - HTTP PUT
  - Редактирование - HTTP PATCH
  - Удаление - HTTP DELETE
- Валидация полей при создании и модификации данных.
- Логирование методов модификации и записи данных.

## Сущности и их атрибуты
### Пользователь
- ФИО
- Пол
- Дата рождения
- Адрес проживания (текст)

### Телефоны
- ID пользователя
- Вид (Городской/Мобильный)
- Номер телефона

### Электронные адреса
- ID пользователя
- Вид (Личная/Рабочая)
- Email

## Технологии
- Python 3.10
- PostgreSQL 14

## Инструкция по установке и запуску
1. Создайте виртуальное окружение:
```
python -m venv venv
```
3. Активируйте виртуальное окружение:
- Для Windows:
  ```
  venv\Scripts\activate
  ```
- Для Unix или MacOS:
  ```
  source venv/bin/activate
  ```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Создайте таблицы в базе данных:
```
psql -U username -d dbname -a -f schema.sql
```
5. Добавьте данные в файл `config.ini` согласно вашим настройкам базы данных.
6. Заполните базу данных:
```
python seed.py
```
7. Запустите приложение:
```
python main.py
```
8. Откройте в браузере:
http://127.0.0.1:8000/docs
