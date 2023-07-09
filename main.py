import logging
import asyncio

import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Dispatcher, Bot
from aio_things.handlers import router


async def main() -> None:
    """
    
    dp - Обрабатывает входящие обновления

    bot - Токен бота. parse_mode - вид форматирования текста
    
    dp.include_router - подключение запросов из другого файла 
    
    bot.delete_webhook(drop_pending_updates = True) - Удаляет все обновления/сообщения которые приходят в бот после отключения
    
    dp.start_polling(bot) - Запускаеться поиск обновлений/сообщений для бота
    
    load_dotenv(find_dotenv()) - находит файл .env и забирает строку под названием TOKEN
    """
    load_dotenv(find_dotenv())
    token = os.environ.get('TOKEN')
    dp = Dispatcher()
    bot = Bot(token, parse_mode= 'HTML')
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates= True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    """
    logging.basicConfig(level= logging.INFO) - Вывод информации о том, чт опроисходит с ботом в консоль
    """
    logging.basicConfig(level= logging.INFO)
    asyncio.run(main())
