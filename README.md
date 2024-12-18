# EnergyFlow

EnergyFlow — это веб-приложение на Python с использованием Flask и SQLite, предназначенное для управления пользователями и их профилями, включая функционал администратора для фильтрации данных.

---

## Функционал приложения

### Для обычных пользователей:
- Регистрация и вход в систему.
- Обновление личного профиля (рост, вес, пол).
- Выход из системы.

### Для администратора:
- Просмотр списка всех зарегистрированных пользователей.
- Фильтрация пользователей по имени, email, росту, весу и полу.
- Управление пользователями.

---

## Установка и запуск приложения

### 1. Клонирование репозитория
Склонируйте репозиторий на ваш локальный компьютер:

```bash
git clone https://github.com/<ваш-логин>/EnergyFlow.git
cd EnergyFlow
```

### 2. Установка зависимостей
Убедитесь, что у вас установлен Python версии 3.8 или выше. Затем установите все необходимые зависимости:

```bash
pip install -r requirements.txt
```

Если файл `requirements.txt` отсутствует, его можно создать с помощью:

```bash
pip freeze > requirements.txt
```

### 3. Создание базы данных
Приложение использует SQLite для хранения данных. Для инициализации базы данных выполните следующие команды:

```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 4. Запуск приложения
Запустите сервер разработки Flask:

```bash
python app.py
```

Приложение будет доступно по адресу:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Как создать администратора вручную
Чтобы создать администратора, выполните следующие шаги:

1. Откройте Python-оболочку:

```bash
python
```

2. Импортируйте необходимые модули:

```python
from app import db, User
```

3. Создайте нового администратора:

```python
hashed_password = "ваш_захэшированный_пароль"
admin = User(username="admin", email="admin@example.com", password=hashed_password, is_admin=True)
db.session.add(admin)
db.session.commit()
```

4. Выйдите из оболочки:

```python
exit()
```

Теперь вы можете войти в систему с учетными данными администратора.

---

## Структура проекта

```plaintext
EnergyFlow/
|-- app.py                # Основной файл приложения
|-- templates/            # HTML-шаблоны
|   |-- base.html         # Базовый шаблон
|   |-- index.html        # Главная страница
|   |-- login.html        # Страница входа
|   |-- register.html     # Страница регистрации
|   |-- profile.html      # Страница профиля пользователя
|   |-- admin.html        # Панель администратора
|-- static/               # Статические файлы (CSS, JS, изображения)
|-- requirements.txt      # Зависимости проекта
|-- README.md             # Документация проекта
|-- energyflow.db         # SQLite база данных
```
