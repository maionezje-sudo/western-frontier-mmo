"""
Локации - города и пустошь
"""
from dataclasses import dataclass
from typing import List

@dataclass
class Location:
    name: str
    description: str
    has_bar: bool = True
    has_shop: bool = True
    has_brothel: bool = False
    has_bank: bool = False
    is_wilderness: bool = False

# Карта мира
LOCATIONS = {
    "town": Location(
        name="Санта-Фе",
        description="Главный город. Здесь можно отдохнуть и торговать.",
        has_bar=True, has_shop=True, has_bank=True
    ),
    "dusty": Location(
        name="Пыльный город",
        description="Маленький городок на краю пустоши.",
        has_bar=True, has_shop=True
    ),
    "blackrock": Location(
        name="Блэкрок",
        description="Город шахтёров. Здесь добывают золото.",
        has_bar=True, has_shop=True
    ),
    "border": Location(
        name="Приграничный город",
        description="Опасное место near границы.",
        has_bar=True, has_shop=True, has_brothel=True
    ),
    "wilderness": Location(
        name="Пустошь",
        description="Дикая местность. Здесь можно искать золото и охотиться.",
        is_wilderness=True
    )
}

def get_location_info(loc_id: str) -> Location:
    return LOCATIONS.get(loc_id, LOCATIONS["town"])

def get_all_locations() -> List[str]:
    return list(LOCATIONS.keys())
