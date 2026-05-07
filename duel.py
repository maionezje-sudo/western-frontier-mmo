"""
Дуэли - PvP механика
"""
import random
import time
from config import COOLDOWN_DUEL

class DuelSystem:
    def __init__(self):
        self.cooldowns = {}

    def can_duel(self, user_id: int) -> bool:
        if user_id not in self.cooldowns:
            return True
        return time.time() - self.cooldowns[user_id] >= COOLDOWN_DUEL

    def duel(self, attacker_id: int, defender_id: int, 
             attacker_stats: dict, defender_stats: dict, bet: int = 0) -> dict:
        if not self.can_duel(attacker_id):
            remaining = COOLDOWN_DUEL - (time.time() - self.cooldowns[attacker_id])
            return {"success": False, "message": f"Подожди {int(remaining)} сек. перед следующей дуэлью."}

        attacker_power = attacker_stats["level"] * random.uniform(0.8, 1.2)
        defender_power = defender_stats["level"] * random.uniform(0.8, 1.2)

        if attacker_power > defender_power:
            winner = "attacker"
            reward = bet if bet > 0 else 10
        elif defender_power > attacker_power:
            winner = "defender"
            reward = bet if bet > 0 else 10
        else:
            winner = "draw"
            reward = 0

        self.cooldowns[attacker_id] = time.time()

        return {
            "success": True,
            "winner": winner,
            "reward": reward,
            "attacker_power": round(attacker_power, 1),
            "defender_power": round(defender_power, 1),
            "message": self._format_message(winner, reward, bet)
        }

    def _format_message(self, winner: str, reward: int, bet: int) -> str:
        if winner == "attacker":
            return f"Ты выиграл дуэль! Забрал {reward}$ у противника." if bet > 0 else "Ты выиграл дуэль! Репутация повышена."
        elif winner == "defender":
            return f"Ты проиграл дуэль. Потерял {reward}$." if bet > 0 else "Ты проиграл дуэль. Репутация понижена."
        return "Ничья! Оба остались при своих."

    def get_cooldown(self, user_id: int) -> int:
        if user_id not in self.cooldowns:
            return 0
        return max(0, int(COOLDOWN_DUEL - (time.time() - self.cooldowns[user_id])))
