# Task Manager API

Это проект, реализующий REST API для управления задачами пользователей. С помощью этого API можно создавать, обновлять, удалять и получать задачи, а также управлять учетными записями пользователей через регистрацию и аутентификацию с использованием JWT. 

**task-manager.py** — это скрипт, который позволяет организовать систему управления задачами с возможностью аутентификации пользователей и работы с базой данных.

## Описание

Основные возможности:

- Регистрация и логин пользователей.
- Аутентификация с использованием JWT.
- Полный CRUD функционал для работы с задачами:
  - Создание задач.
  - Получение списка задач.
  - Получение задачи по ID.
  - Обновление задач.
  - Удаление задач.

Каждый пользователь имеет возможность управлять только своими задачами.

## Стек технологий

- **Flask** — веб-фреймворк для Python, используемый для разработки API.
- **Flask-SQLAlchemy** — ORM для взаимодействия с базой данных.
- **Flask-JWT-Extended** — для работы с JSON Web Tokens (JWT) для аутентификации пользователей.
- **Werkzeug** — для безопасного хеширования паролей.
- **SQLite** — база данных для хранения данных о пользователях и задачах (можно изменить на PostgreSQL при необходимости).

## Установка

### Требования

Для работы с проектом необходимо установить Python 3.8+ и следующие библиотеки:

```bash
pip install flask flask_sqlalchemy flask_jwt_extended werkzeug
````

### Настройка базы данных

Скрипт автоматически создает таблицы в базе данных при первом запуске приложения с использованием SQLAlchemy. Для хранения данных используется SQLite по умолчанию, но вы можете настроить подключение к другой базе данных (например, PostgreSQL), изменив конфигурацию в коде.

### Запуск приложения

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Mironov1994/Task-Manager.git
```

2. Перейдите в папку с проектом:

```bash
cd Task-Manager
```

3. Запустите приложение:

```bash
python task-manager.py
```

После запуска приложение будет доступно по адресу `http://127.0.0.1:5000/`.

## Эндпоинты API

### 1. Регистрация нового пользователя

**POST /register**

**Параметры запроса:**

```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "your_password"
}
```

**Ответ:**

```json
{
  "message": "User successfully registered."
}
```

### 2. Авторизация пользователя

**POST /login**

**Параметры запроса:**

```json
{
  "email": "john.doe@example.com",
  "password": "your_password"
}
```

**Ответ:**

```json
{
  "access_token": "jwt_token"
}
```

### 3. Создание задачи

**POST /tasks**

**Параметры запроса:**

```json
{
  "title": "Finish homework",
  "description": "Complete the math homework",
  "due_date": "2025-08-15T10:00:00",
  "priority": 1
}
```

**Ответ:**

```json
{
  "id": 1,
  "title": "Finish homework",
  "description": "Complete the math homework",
  "due_date": "2025-08-15T10:00:00",
  "priority": 1,
  "created_at": "2025-08-11T14:00:00",
  "updated_at": "2025-08-11T14:00:00"
}
```

### 4. Получение списка задач

**GET /tasks**

**Ответ:**

```json
[
  {
    "id": 1,
    "title": "Finish homework",
    "description": "Complete the math homework",
    "due_date": "2025-08-15T10:00:00",
    "priority": 1,
    "created_at": "2025-08-11T14:00:00",
    "updated_at": "2025-08-11T14:00:00"
  }
]
```

### 5. Получение задачи по ID

**GET /tasks/{task\_id}**

**Ответ:**

```json
{
  "id": 1,
  "title": "Finish homework",
  "description": "Complete the math homework",
  "due_date": "2025-08-15T10:00:00",
  "priority": 1,
  "created_at": "2025-08-11T14:00:00",
  "updated_at": "2025-08-11T14:00:00"
}
```

### 6. Обновление задачи

**PUT /tasks/{task\_id}**

**Параметры запроса:**

```json
{
  "title": "Updated title",
  "description": "Updated description",
  "due_date": "2025-08-20T10:00:00",
  "priority": 2
}
```

**Ответ:**

```json
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "due_date": "2025-08-20T10:00:00",
  "priority": 2,
  "created_at": "2025-08-11T14:00:00",
  "updated_at": "2025-08-11T14:05:00"
}
```

### 7. Удаление задачи

**DELETE /tasks/{task\_id}**

**Ответ:**

```json
{
  "message": "Task deleted successfully."
}
```

## Лицензия

Этот проект распространяется под лицензией **MIT**. См. файл [LICENSE](LICENSE) для подробной информации.
