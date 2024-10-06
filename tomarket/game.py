import asyncio
import random
from typing import Any
import httpx
from env import Env
from tomarket.endpoints import Endpoints

from utils.loggy import logger


class GameAction:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    async def _play(self) -> bool:
        response = await self.http_client.post(
            Endpoints.GAME_PLAY,
            json={"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"},
        )
        match response.status_code:
            case 200:
                logger.success("Successfully started the game.")
                return True
            case _:
                logger.error(f"Failed to start the game: {response.status_code}")
                logger.debug(response.json())
                return False

    async def _claim(self, points: int) -> bool:
        json_payload: dict[str, Any] = {
            "game_id": "59bcd12e-04e2-404c-a172-311a0084587d"
        }
        if points is not None:
            json_payload["points"] = points

        response = await self.http_client.post(
            Endpoints.GAME_CLAIM,
            json=json_payload,
        )
        match response.status_code:
            case 200:
                logger.success("Sucessfully claimed")
                return True
            case _:
                logger.error(f"Failed to claim game: {response.status_code}")
                logger.debug(response.json())
                return False

    async def play_game(self) -> bool:
        is_started = await self._play()
        if not is_started:
            return False
        points: int = random.randint(Env.MIN_POINTS, Env.MAX_POINTS)
        logger.info(f"Points yet to be claimed: {points}")
        logger.info("Playing Game wait for 30 seconds")
        await asyncio.sleep(30)
        return await self._claim(points)
