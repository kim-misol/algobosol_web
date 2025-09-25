from __future__ import annotations
from typing import Optional
from cachetools import TTLCache
from utils.config import SETTINGS

class PriceService:
    """증권사 API를 여기로 어댑팅"""
    def __init__(self, ttl_seconds: int = SETTINGS.price_ttl_seconds) -> None:
        self._cache = TTLCache(maxsize=2048, ttl=ttl_seconds)

    def get_current_price(self, name_or_symbol: str) -> Optional[float]:
        if not name_or_symbol:
            return None
        key = name_or_symbol.strip()
        if key in self._cache:
            return self._cache[key]

        # TODO: 실제 API 연동 (예: broker.get_price(key))
        price = round(max(1, len(key)) * 123.45, 2)  # 데모
        self._cache[key] = price
        return price

price_service = PriceService()
