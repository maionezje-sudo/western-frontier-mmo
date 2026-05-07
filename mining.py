"""
Копание золота - кликер механика
"""
import random
import time
from config import COOLDOWN_MINING

class Mining:
    def __init__(self):
        self.cooldowns = {}

    def can_mine(self, user_id: int) -> bool:
        if user_id not in self.cooldowns:
            return True
        return time.time() - self.cooldowns[user_id] >= COOLDOWN_MINING

    def mine(self, user_id: int) -> dict:
        if not self.can_mine(user_id):
            remaining = COOLDOWN_MINING - (time.time() - self.cooldowns[user_id])
            return {"success": False, "gold": 0, "message": f"Отдохни ещё {int(remaining)} сек."}

        roll = random.random()
        if roll < 0.1:
            gold = random.randint(5, 10)
            message = f"Большая удача! Нашёл {gold} золота!"
        elif roll < 0.4:
            gold = random.randint(2, 5)
            message = f"Нашёл {gold} золота."
        else:
            gold = random.randint(0, 2)
            message = "Увы, ничего не нашёл..." if gold == 0 else f"Нашёл {gold} золота."

        self.cooldowns[user_id] = time.time()
        return {"success": True, "gold": gold, "message": message}

    def get_cooldown(self, user_id: int) -> int:
        if user_id not in self.cooldowns:
            return 0
        return max(0, int(COOLDOWN_MINING - (time.time() - self.cooldowns[user_id])))
