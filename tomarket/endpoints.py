from typing import Final


class Endpoints:
    _API: Final[str] = "https://api-web.tomarket.ai/tomarket-game/v1"
    LOGIN: Final[str] = f"{_API}/user/login"
    USER_BALANCE: Final[str] = f"{_API}/user/balance"
    DAILY_CLAIM: Final[str] = f"{_API}/daily/claim"
    FARM_START: Final[str] = f"{_API}/farm/start"
    FARM_CLAIM: Final[str] = f"{_API}/farm/claim"
    GAME_PLAY: Final[str] = f"{_API}/game/play"
    GAME_CLAIM: Final[str] = f"{_API}/game/claim"
