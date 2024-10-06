from typing import Optional
import httpx
from loguru import logger
from env import Env
from telegram.tgClient import TGClient
from tomarket.game import GameAction
from tomarket.farm import FarmAction
from tomarket.endpoints import Endpoints
from fake_useragent import UserAgent

from tomarket.platform import Platform


class Tomarket:
    def __init__(
        self,
        peer_id: str,
        http_timeout: float = 60 * 2,
        platform: Platform = Platform.ANDROID,
    ):
        self.peer_id = peer_id
        self.http_client = httpx.AsyncClient(
            timeout=http_timeout,
            headers={
                "User-Agent": UserAgent(os=platform.value).random,
            },
        )
        self.game = GameAction(self.http_client)
        self.farm = FarmAction(self.http_client)

    async def login(self) -> Optional[bool]:
        self.http_client.headers.pop("Authorization", None)
        tg_client = TGClient()
        query = await tg_client.get_query_string(self.peer_id)
        if query.is_err():
            logger.error(f"Query Retrieval Failed - Reason: {query.value}")
            return False
        response = await self.http_client.post(
            Endpoints.LOGIN,
            json={"init_data": query.value, "invite_code": Env.REF_ID},
        )

        access_token = response.json().get("data", {}).get("access_token")
        if access_token:
            self.http_client.headers["Authorization"] = f"{access_token}"
            logger.success("Tomarket Login successful")
            return True

    async def get_balance(self) -> Optional[dict]:
        response = await self.http_client.post(Endpoints.USER_BALANCE)
        if response.status_code == 200:
            return response.json()
        logger.error("Unable to Obtain User Balance")
        logger.debug(f"Status Code: {response.status_code}")
        logger.debug(response.json())

    async def play_passes_left(self) -> int:
        balance = await self.get_balance()
        if balance is None:
            return 0
        passes_left = balance.get("data", {}).get("play_passes", 0)
        logger.info(f"Passes Left: {passes_left}")
        return passes_left

    async def claim_daily(self) -> Optional[int]:
        """
        Returns the next claim date in seconds
        """
        resp = await self.http_client.post(
            Endpoints.DAILY_CLAIM,
            json={"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"},
        )
        match resp.status_code:
            case 200:
                resp_json = resp.json()
                message = resp_json.get("message")
                if message and "already_check" in message:
                    logger.info("Daily Claim Already Claimed")
                else:
                    points = resp_json.get("data", {}).get("today_points")
                    logger.success(f"Daily Claim Successful: {points} Points")
                return resp_json.get("data", {}).get("next_check_ts")
            case _:
                logger.error(f"Daily Claim Failed: {resp.status_code}")
                logger.debug(resp.json())
