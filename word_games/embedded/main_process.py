from .game_process import GameInterface
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

            # self.process = DiodeInterface()
            # self.process.run()
        # if game_no == 1:
        #     self.calibrate_process = CalibrateInterface()
        #     self.calibrate_process.run()
        # elif game_no == 2:
        #     self.diode_process = DiodeInterface()
        #     self.diode_process.run()
        # else:
        #     self.rule_process = RuleInterface()
        #     self.rule_process.run()

    

    def on_init(self):
        logger.info("Initialisig listening")
        self.message_interface.send(json.dumps(
            {
                "win": False,
            }
        ))
