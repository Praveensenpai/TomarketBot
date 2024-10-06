import asyncio
from contextlib import suppress
import random
import time
from tomarket.tomarket import Tomarket
from utils.dt import secs_to_dt
from utils.loggy import logger
from timecalculator import TimeCalculator


class TomarketBot:
    def __init__(self, concurrency: int = 1) -> None:
        self.semaphore = asyncio.Semaphore(concurrency)

    async def farming_task(self, tomarket: Tomarket):
        await asyncio.sleep(1)
        async with self.semaphore:
            current_time = int(time.time())
            balance = await tomarket.get_balance()
            if not balance:
                return
            data = balance["data"]
            farming_data = data.get("farming", {})

            if not farming_data:
                logger.info("Starting farming...")
                await tomarket.farm.start()
                return

            start_at = farming_data["start_at"]
            end_at = farming_data["end_at"]

            if current_time > end_at:
                logger.info("Harvesting...")
                await tomarket.farm.harvest()

        if start_at < current_time < end_at:
            async with self.semaphore:
                logger.info("Farming is still running.")
                time_until_claim = end_at - current_time + 60
                logger.info(
                    f"Sleeping for {time_until_claim} seconds until claiming..."
                )
                logger.info(f"Minutes: {time_until_claim / TimeCalculator.MINUTE}")
                logger.info(f"Hours {time_until_claim / TimeCalculator.HOUR}")

            await asyncio.sleep(time_until_claim)

            async with self.semaphore:
                logger.info("Harvesting...")
                await tomarket.farm.harvest()

    async def gaming_task(self, tomarket: Tomarket):
        await asyncio.sleep(15)
        async with self.semaphore:
            pass_left = await tomarket.play_passes_left()
            logger.info(f"Passes left: {pass_left}")
            for ps in range(1, pass_left + 1):
                logger.info(f"[{ps}] Playing Game...")
                await asyncio.sleep(random.randint(2, 6))
                await tomarket.game.play_game()

    async def daily_claim_task(self, tomarket: Tomarket):
        async with self.semaphore:
            logger.info("Claiming Daily...")
            await asyncio.sleep(random.randint(2, 6))
            next_claim = await tomarket.claim_daily()
            if next_claim is None:
                return
            logger.info(f"Next Daily Claim: {secs_to_dt(next_claim)}")

    async def main(self):
        while True:
            try:
                tomarket = Tomarket("Tomarket_ai_bot")
                is_logged_in = await tomarket.login()
                if not is_logged_in:
                    return

                await self.daily_claim_task(tomarket)

                tasks = [
                    self.farming_task(tomarket),
                    self.gaming_task(tomarket),
                ]
                await asyncio.gather(*tasks)
                logger.info(
                    f"Rest Period: Sleepng for {TimeCalculator.HOUR *  0.25} seconds"
                )
                await asyncio.sleep(TimeCalculator.HOUR * 0.25)
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                logger.info(f"Sleepng for {TimeCalculator.HOUR * 1} seconds")
                await asyncio.sleep(TimeCalculator.HOUR * 1)

    def run(self):
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.main())
            except Exception as e:
                logger.error(f"Restarting event loop due to error: {e}")
            finally:
                with suppress(Exception):
                    loop.close()
                logger.info("Restarting the main loop...")
                time.sleep(10)


if __name__ == "__main__":
    TomarketBot().run()
