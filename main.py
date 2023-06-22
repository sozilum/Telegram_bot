import logging
import asyncio

from aiogram import Dispatcher, Bot
from aio_things.handlers import router


async def main() -> None:
    """
    
    dp - Обрабатывает входящие обновления

    bot - Токен бота. parse_mode - вид форматирования текста
    
    dp.include_router - подключение запросов из другого файла 
    
    bot.delete_webhook(drop_pending_updates = True) - Удаляет все обновления/сообщения которые приходят в бот после отключения
    
    dp.start_polling(bot) - Запускаеться поиск обновлений/сообщений для бота
    """
    dp = Dispatcher()
    bot = Bot('6070000442:AAEaCJxrYOuTQt5ZA_YdTzaq6KTH_Vbw1ho', parse_mode= 'HTML')
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates= True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    """
    logging.basicConfig(level= logging.INFO) - Вывод информации о том, чт опроисходит с ботом в консоль
    """
    logging.basicConfig(level= logging.INFO)
    asyncio.run(main())