"""
Торговля - механика купли-продажи
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class Item:
    name: str
    buy_price: int
    sell_price: int
    description: str = ""

ITEMS = {
    "whiskey": Item("Виски", 10, 5, "Крепкий напиток"),
    "horse": Item("Лошадь", 100, 70, "Средство передвижения"),
    "gun": Item("Револьвер", 200, 150, "Оружие для дуэлей"),
    "dynamite": Item("Динамит", 50, 30, "Взрывчатка"),
    "medicine": Item("Лекарства", 30, 15, "Восстанавливает здоровье")
}

CITY_PRICES = {
    "town": {"whiskey": 1.0, "horse": 1.0, "gun": 1.0, "dynamite": 1.0, "medicine": 1.0},
    "dusty": {"whiskey": 0.8, "horse": 1.2, "gun": 1.1, "dynamite": 0.9, "medicine": 1.2},
    "blackrock": {"whiskey": 1.2, "horse": 1.1, "gun": 0.9, "dynamite": 0.8, "medicine": 1.0},
    "border": {"whiskey": 1.5, "horse": 0.8, "gun": 1.2, "dynamite": 1.3, "medicine": 0.8},
}

class TradeSystem:
    def __init__(self):
        self.inventory = {}

    def get_price(self, item_id: str, city: str) -> tuple:
        if item_id not in ITEMS:
            return None, None
        item = ITEMS[item_id]
        multiplier = CITY_PRICES.get(city, {}).get(item_id, 1.0)
        buy_price = int(item.buy_price * multiplier)
        sell_price = int(item.sell_price * multiplier * 0.9)
        return buy_price, sell_price

    def buy(self, user_id: int, item_id: str, city: str, money: int) -> dict:
        if item_id not in ITEMS:
            return {"success": False, "message": "Такого предмета нет."}
        buy_price, _ = self.get_price(item_id, city)
        if money < buy_price:
            return {"success": False, "message": f"Нужно {buy_price}$, у тебя {money}$."}
        if user_id not in self.inventory:
            self.inventory[user_id] = {}
        self.inventory[user_id][item_id] = self.inventory[user_id].get(item_id, 0) + 1
        return {"success": True, "money_spent": buy_price, "message": f"Купил {ITEMS[item_id].name} за {buy_price}$."}

    def sell(self, user_id: int, item_id: str, city: str) -> dict:
        if user_id not in self.inventory or item_id not in self.inventory[user_id]:
            return {"success": False, "message": "У тебя этого нет."}
        _, sell_price = self.get_price(item_id, city)
        self.inventory[user_id][item_id] -= 1
        return {"success": True, "money_earned": sell_price, "message": f"Продал {ITEMS[item_id].name} за {sell_price}$."}

    def get_inventory(self, user_id: int) -> Dict[str, int]:
        return self.inventory.get(user_id, {})
