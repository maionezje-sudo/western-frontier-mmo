"""
Обработчики команд бота
"""
from aiogram import types
from aiogram.filters import Command
from players import PlayersDB
from locations import LOCATIONS, get_location_info
from mining import Mining
from duel import DuelSystem
from trade import TradeSystem, ITEMS
from config import GAME_CURRENCY, MAX_HEALTH, MAX_ENERGY

players_db = PlayersDB()
mining = Mining()
duel_system = DuelSystem()
trade_system = TradeSystem()

async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    player = await players_db.get_player(user_id)
    if player:
        await message.answer(
            f"С возвращением, {player.name}!\n"
            f"Ты в локации: {get_location_info(player.location).name}\n\n"
            f"💰 Деньги: {player.money}{GAME_CURRENCY}\n"
            f"💎 Золото: {player.gold}\n"
            f"❤️ Здоровье: {player.health}/{MAX_HEALTH}\n"
            f"⚡ Энергия: {player.energy}/{MAX_ENERGY}\n"
            f"📍 Уровень: {player.level}"
        )
    else:
        player = await players_db.create_player(user_id, name)
        await message.answer(
            f"Добро пожаловать в Western Frontier, {name}!\n\n"
            f"Ты приехал в Санта-Фе с {player.money}${GAME_CURRENCY} в кармане.\n"
            f"Твоя цель — выжить, заработать состояние и стать легендой Дикого Запада!\n\n"
            f"Используй /help для списка команд."
        )

async def cmd_help(message: types.Message):
    help_text = """
🎮 <b>Команды Western Frontier</b>

<b>Основные:</b>
/start — Профиль и статистика
/profile — Твой профиль
/locations — Список локаций
/travel [город] — Переместиться

<b>Заработок:</b>
/mine — Копать золото (пустошь)
/trade — Торговля

<b>PvP:</b>
/duel [игрок] [ставка] — Вызвать на дуэль

<b>Разное:</b>
/bar — Зайти в бар
/shop — Магазин
/clan — Клан (скоро)
/help — Эта справка
    """
    await message.answer(help_text, parse_mode="HTML")

async def cmd_profile(message: types.Message):
    user_id = message.from_user.id
    player = await players_db.get_player(user_id)
    if not player:
        await message.answer("Сначала зарегистрируйся: /start")
        return
    location = get_location_info(player.location)
    text = f"""
👤 <b>{player.name}</b>
📍 Локация: {location.name}

💰 Деньги: {player.money}{GAME_CURRENCY}
💎 Золото: {player.gold}

❤️ Здоровье: {player.health}/{MAX_HEALTH}
⚡ Энергия: {player.energy}/{MAX_ENERGY}

📊 Уровень: {player.level}
⭐ Опыт: {player.exp}
🏆 Побед: {player.wins} | Поражений: {player.losses}
    """
    await message.answer(text, parse_mode="HTML")

async def cmd_locations(message: types.Message):
    text = "<b>🗺️ Локации:</b>\n\n"
    for loc_id, loc in LOCATIONS.items():
        text += f"• <b>{loc.name}</b> — {loc.description}\n"
    text += "\n/travel [город] — переместиться"
    await message.answer(text, parse_mode="HTML")

async def cmd_travel(message: types.Message, city: str):
    user_id = message.from_user.id
    player = await players_db.get_player(user_id)
    if not player:
        await message.answer("Сначала зарегистрируйся: /start")
        return
    city_map = {
        "санта-фе": "town", "town": "town",
        "пыльный": "dusty", "dusty": "dusty",
        "блэкрок": "blackrock", "blackrock": "blackrock",
        "приграничный": "border", "border": "border",
        "пустошь": "wilderness", "wilderness": "wilderness"
    }
    city_key = city_map.get(city.lower())
    if not city_key:
        await message.answer("Неизвестный город. /locations — список.")
        return
    if city_key == player.location:
        await message.answer("Ты уже там.")
        return
    player.location = city_key
    await players_db.update_player(player)
    loc = get_location_info(city_key)
    await message.answer(f"Переместился в {loc.name}!\n{loc.description}")

async def cmd_mine(message: types.Message):
    user_id = message.from_user.id
    player = await players_db.get_player(user_id)
    if not player:
        await message.answer("Сначала зарегистрируйся: /start")
        return
    if player.location != "wilderness":
        await message.answer("Золото можно искать только в пустоши! /travel пустошь")
        return
    result = mining.mine(user_id)
    if result["success"]:
        player.gold += result["gold"]
        await players_db.update_player(player)
        await message.answer(f"⛏️ {result['message']}\n\nНашёл: +{result['gold']} 💎")
    else:
        await message.answer(result["message"])

async def cmd_shop(message: types.Message):
    text = "<b>🛒 Магазин:</b>\n\n"
    for item_id, item in ITEMS.items():
        text += f"• {item.name} — {item.buy_price}${GAME_CURRENCY}\n"
    text += "\n/buy [предмет] — купить\n/sell [предмет] — продать"
    await message.answer(text, parse_mode="HTML")

async def cmd_bar(message: types.Message):
    user_id = message.from_user.id
    player = await players_db.get_player(user_id)
    if not player:
        await message.answer("Сначала зарегистрируйся: /start")
        return
    location = get_location_info(player.location)
    if not location.has_bar:
        await message.answer("В этом городе нет бара.")
        return
    await message.answer(
        "🍺 <b>Бар</b>\n\n"
        "Здесь можно:\n"
        "• Выпить виски (+энергия)\n"
        "• Послушать сплетни\n"
        "• Найти противника для дуэли\n\n"
        "/drink — выпить (10$)",
        parse_mode="HTML"
    )
