"""
Регистрация всех обработчиков
"""
from aiogram import Dispatcher
from aiogram.filters import Command
import commands

def register_handlers(dp: Dispatcher):
    dp.message.register(commands.cmd_start, Command("start"))
    dp.message.register(commands.cmd_help, Command("help"))
    dp.message.register(commands.cmd_profile, Command("profile"))
    dp.message.register(commands.cmd_locations, Command("locations"))
    dp.message.register(commands.cmd_mine, Command("mine"))
    dp.message.register(commands.cmd_shop, Command("shop"))
    dp.message.register(commands.cmd_bar, Command("bar"))
