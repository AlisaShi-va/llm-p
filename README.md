## API для работы с большой языковой моделью
### Установка и запуск проекта через uv
- Установка uv
   pip install uv
- Инициализация проекта
   uv init 
- Создание виртуального окружения
   uv venv
- Активация виртуального окружения
  .venv\Scripts\activate.bat
- Установка зависимостей проекта
  uv pip install -r <(uv pip compile pyproject.toml)

### Структура проекта
llm_p/
├── pyproject.toml                 # Зависимости проекта (uv)
├── README.md                      # Описание проекта и запуск
├── .env.example                   # Пример переменных окружения
│
├── app/
│   ├── init.py
│   ├── main.py                    # Точка входа FastAPI
│   │
│   ├── core/                      # Общие компоненты и инфраструктура
│   │   ├── init.py
│   │   ├── config.py              # Конфигурация приложения (env → Settings)
│   │   ├── security.py            # JWT, хеширование паролей
│   │   └── errors.py              # Доменные исключения
│   │
│   ├── db/                        # Слой работы с БД
│   │   ├── init.py
│   │   ├── base.py                # DeclarativeBase
│   │   ├── session.py             # Async engine и sessionmaker
│   │   └── models.py              # ORM-модели (User, ChatMessage)
│   │
│   ├── schemas/                   # Pydantic-схемы (вход/выход API)
│   │   ├── init.py
│   │   ├── auth.py                # Регистрация, логин, токены
│   │   ├── user.py                # Публичная модель пользователя
│   │   └── chat.py                # Запросы и ответы LLM
│   │
│   ├── repositories/              # Репозитории (ТОЛЬКО SQL/ORM)
│   │   ├── init.py
│   │   ├── users.py               # Доступ к таблице users
│   │   └── chat_messages.py       # Доступ к истории чатов
│   │
│   ├── services/                  # Внешние сервисы
│   │   ├── init.py
│   │   └── openrouter_client.py   # Клиент OpenRouter / LLM
│   │
│   ├── usecases/                  # Бизнес-логика приложения
│   │   ├── init.py
│   │   ├── auth.py                # Регистрация, логин, профиль
│   │   └── chat.py                # Логика общения с LLM
│   │
│   └── api/                       # HTTP-слой (тонкие эндпоинты)
│       ├── init.py
│       ├── deps.py                # Dependency Injection
│       ├── routes_auth.py         # /auth/*
│       └── routes_chat.py         # /chat/*
│
└── app.db                         # SQLite база (создаётся при запуске)

### Эндпоинты
<img width="458" height="430" alt="chrome_JUjC5T4NB3" src="https://github.com/user-attachments/assets/fb5fd8a0-c672-4167-97b4-0375610f3faf" />

- Регистрация пользователя POST /auth/register
<img width="546" height="442" alt="LcepbSYiIG" src="https://github.com/user-attachments/assets/efd50f23-33da-4d18-a8e1-85fd9cdc0496" />

- Получение токена POST /auth/login
<img width="1518" height="927" alt="chrome_IEuDht6vLm" src="https://github.com/user-attachments/assets/2c4b718d-ffb6-474f-a731-cf4ddac74299" />

- Авторизация (в Swagger)
<img width="567" height="374" alt="chrome_kCkvGRsLkZ" src="https://github.com/user-attachments/assets/cd43fce1-2607-4e3c-bf74-65f362d76201" />
<img width="556" height="345" alt="chrome_1MSEycwNbw" src="https://github.com/user-attachments/assets/14a57d8a-896c-4724-a576-e38b69d4b610" />

- Получение информмации о текущем пользователе GET /auth/me
<img width="724" height="401" alt="chrome_gl1p8LqGCk" src="https://github.com/user-attachments/assets/55617fb2-cf3d-49c7-b15e-48ce29cc25af" />

- Запрос в чат POST /chat
<img width="380" height="355" alt="chrome_Mn3EUfMtsd" src="https://github.com/user-attachments/assets/a9e43f50-e67f-41e5-be12-9842ecbf3432" />

- Получение истории GET /chat/history
<img width="466" height="350" alt="chrome_KMJsFAQmzi" src="https://github.com/user-attachments/assets/b0821dd4-206a-437b-a3f3-7cd00b2d03e9" />

- Удаление истории DELETE /chat/history
<img width="471" height="262" alt="chrome_cgXH4wOcMg" src="https://github.com/user-attachments/assets/ddec17d0-8015-405a-96d3-6c865d9968f8" />

- Проверка состояния приложения GET /health
<img width="469" height="269" alt="chrome_vJKLHJlnLi" src="https://github.com/user-attachments/assets/dbd3a670-b616-4e09-90dd-285e0852e1df" />
 
