# Торговый бот для Telegram
---

Бот предназначен для отслеживания акций/валюты на любой из существующих бирж, например NASDAQ или MOEX.


# Установка
---


1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Измените название файла `settings.py.example`, убрав из него `.example` и впишите в него собственные API ключи и переменные окружения
5. Установите docker для вашей ОС
6. Запустите локальные БД для работы Celery:
```
docker run -d -p 5672:5672 rabbitmq
docker run -d -p 6379:6379 redis
```
7. Запустите celery командой `celery -A tasks worker --loglevel=info`
8. Запустите бота `python main.py`


# Фоновый запуск
---

Для нового запуска бота на сервере можно использовать конфигурацию для supervisord

Конфигурация для Celery:

	[program:celery]
	command = PATH/alyzing-trading-bot/env/bin/celery -A tasks worker --loglevel=info
	directory = PATH/analyzing-trading-bot
	user = USER
	autostart = true
	autorestart = true
	startretries = 3
  
  
Конфигурация для бота:

	[program:bot-stock-tracker]
	command = bash -c 'sleep 5 && PATH/analyzing-trading-bot/env/bin/python3.6 PATH/analyzing-trading-bot/main.py'
	directory = PATH/analyzing-trading-bot
	user = USER
	autostart = true
	autorestart = true
	startretries = 3
