from .game_process import GameInterface, DiodeInterface
from .utils import logger_config
import random 
import dotenv 
import json
import os

dotenv.load_dotenv()
logger = logger_config()

import asyncio
import telegram


async def bot_inform():
    bot = telegram.Bot(os.environ["TOKEN"])
    async with bot:
        print(await bot.send_message())



class Orlowski(GameInterface):
    def __init__(self, port, baud_rate)  -> None:
        super().__init__(port, baud_rate=baud_rate)

    def on_message(self, message):
        print(message)
        # do something with the message
        # send a message back
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            logger.error(message)
            return 
        
        if (message['init']):
            logger.info("Received init message, starting calibration")
            # launch individual game processes
            
            # pick a random 
            game_no = random.randint(0, 2)
            logger.info(f"Game {game_no} launched")
            port = '/dev/ttyACM1'
            br = 9600
            process = DiodeInterface(
                port=port, baud_rate=br
            )
            self.launch_process(process)
            # self.process.run()


    def launch_process(self, process):
        import multiprocessing as mp 
        p = mp.Process(
            target=process.run
        )
        p.run()
        p.join()

    def on_init(self):
        logger.info("Initialisig listening")