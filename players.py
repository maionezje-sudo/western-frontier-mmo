"""
Модуль игроков - данные и состояние
"""
import aiosqlite
from dataclasses import dataclass
from typing import Optional
from config import STARTING_MONEY, STARTING_GOLD, MAX_HEALTH, MAX_ENERGY

@dataclass
class Player:
    user_id: int
    name: str
    money: int = STARTING_MONEY
    gold: int = STARTING_GOLD
    health: int = MAX_HEALTH
    energy: int = MAX_ENERGY
    level: int = 1
    exp: int = 0
    location: str = "town"
    clan: Optional[str] = None
    reputation: int = 0
    wins: int = 0
    losses: int = 0

class PlayersDB:
    def __init__(self, db_path="players.db"):
        self.db_path = db_path

    async def init(self):
        """Создание таблицы игроков"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    money INTEGER DEFAULT ?,
                    gold INTEGER DEFAULT ?,
                    health INTEGER DEFAULT ?,
                    energy INTEGER DEFAULT ?,
                    level INTEGER DEFAULT 1,
                    exp INTEGER DEFAULT 0,
                    location TEXT DEFAULT 'town',
                    clan TEXT,
                    reputation INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0
                )
            """, (STARTING_MONEY, STARTING_GOLD, MAX_HEALTH, MAX_ENERGY))
            await db.commit()

    async def get_player(self, user_id: int) -> Optional[Player]:
        """Получить игрока"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM players WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return Player(
                        user_id=row["user_id"],
                        name=row["name"],
                        money=row["money"],
                        gold=row["gold"],
                        health=row["health"],
                        energy=row["energy"],
                        level=row["level"],
                        exp=row["exp"],
                        location=row["location"],
                        clan=row["clan"],
                        reputation=row["reputation"],
                        wins=row["wins"],
                        losses=row["losses"]
                    )
        return None

    async def create_player(self, user_id: int, name: str) -> Player:
        """Создать нового игрока"""
        player = Player(user_id=user_id, name=name)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO players (user_id, name, money, gold, health, energy)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (player.user_id, player.name, player.money, player.gold,
                   player.health, player.energy))
            await db.commit()
        return player

    async def update_player(self, player: Player):
        """Обновить данные игрока"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE players SET 
                    name=?, money=?, gold=?, health=?, energy=?,
                    level=?, exp=?, location=?, clan=?, 
                    reputation=?, wins=?, losses=?
                WHERE user_id=?
            """, (player.name, player.money, player.gold, player.health,
                   player.energy, player.level, player.exp, player.location,
                   player.clan, player.reputation, player.wins, player.losses,
                   player.user_id))
            await db.commit()
