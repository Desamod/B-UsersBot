[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/b_usersbot/join?startapp=ref-5VpQcGPE8TAeULDoUQtCFq)

## Рекомендация перед использованием

# 🔥🔥 Используйте PYTHON 3.10 🔥🔥

> 🇪🇳 README in english available [here](README.md)

## Функционал  
| Функционал                                               | Поддерживается |
|----------------------------------------------------------|:--------------:|
| Многопоточность                                          |       ✅        |
| Поддержка tdata / pyrogram .session / telethon .session  |       ✅        |
| Привязка прокси к сессии                                 |       ✅        |
| Авторегистрация в боте                                   |       ✅        |
| Авто выполнение заданий                                  |       ✅        |



## [Настройки](https://github.com/Desamod/B-UsersBot/blob/master/.env-example/)
| Настройка               |                                Описание                                 |
|-------------------------|:-----------------------------------------------------------------------:|
| **API_ID / API_HASH**   |          Данные платформы, с которой запускать сессию Telegram          | 
| **SLEEP_TIME**          |         Время сна между циклами (по умолчанию - [7200, 10800])          |
| **AUTO_TASK**           |               Автовыполнение тасок (по умолчанию - True)                |
| **JOIN_CHANNELS**       |        Авто-подписка на ТГ каналы из тасок (по умолчанию - True)        |
| **REF_ID**              |                   Реф. ссылка для регистрации в боте                    |
| **USE_PROXY_FROM_FILE** | Использовать-ли прокси из файла `bot/config/proxies.txt` (True / False) |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл run.bat на Windows или run.sh на Линукс

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/Desamod/B-UsersBot) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/Desamod/B-UsersBot
cd B-UsersBot
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/BoolBot >>> python3 main.py --action (1/2)
# Or
~/BoolBot >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/B-UsersBot >>> python main.py --action (1/2)
# Или
~/B-UsersBot >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


### Контакты

Для поддержки или вопросов, вы можете связаться со мной

[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/desforge_cryptwo)

