"""
Western Frontier - MMO бот в жанре вестерн
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    """Запуск бота"""
    logger.info("Western Frontier Bot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
