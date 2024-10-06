import httpx
from tomarket.endpoints import Endpoints
from utils.loggy import logger


class FarmAction:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    async def start(self) -> None:
        response = await self.http_client.post(
            Endpoints.FARM_START,
            json={"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"},
        )
        match response.status_code:
            case 200:
                logger.success("Farming started successfully")
            case _:
                logger.error("Farming start failed: Unexpected status code")
                logger.debug(response.json())

    async def harvest(self) -> None:
        response = await self.http_client.post(
            Endpoints.FARM_CLAIM,
            json={"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"},
        )
        match response.status_code:
            case 200:
                points = response.json()["data"]["points"]
                logger.success(f"Successfully harvested points: {points}")
            case _:
                logger.error(f"Failed to harvest points: {response.status_code}")
                logger.debug(response.json())
