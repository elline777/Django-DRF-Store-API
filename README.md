# Store API (Django DRF)

API товарного склада.

### Домашнее задание по Django rest framework

Курс "Профессия: Python-разработчик", PRODUCTSTAR


## Запуск проекта
1) Клонируем репозиторий
```
    git clone https://github.com/elline777/Django-DRF-Store-API.git    
```
2) Устанавливаем и активируем виртуальное окружение
```
    cd Django-DRF-Store-API
    python -m venv <environment name>
```
- Активация на Linux:
```
    source <environment name>/bin/activate
```    
-  Активация на Windows:
```
    .\<environment name>\Scripts\activate
```
3) Устанавливаем зависимости
```
    pip install -r requirements.txt
```
4) Создаем и запускаем миграции
```
    python manage.py makemigrations 
    python manage.py migrate
```
5) Создаем суперпользователя
```
    python manage.py createsuperuser
```
6) Запускаем сервер
```
    python manage.py runserver
```
