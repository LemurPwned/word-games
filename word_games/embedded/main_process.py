
from .game_process import CalibrateInterface, DiodeInterface, RuleInterface
from .interface import MessageInterface
from .utils import logger_config
import random 
import dotenv 
import os

dotenv.load_dotenv()
logger = logger_config()

import asyncio
import telegram


async def bot_launch():
    bot = telegram.Bot(os.environ["TOKEN"])
    async with bot:
        print(await bot.get_me())



class Orlowski:
    def __init__(self) -> None:
        self.message_interface = MessageInterface(port="/dev/ttyUSB0",
        baud_rate=9600,
        read_interval=0.05)

    def on_message(self, message):
        # do something with the message
        # send a message back
        logger.info("Received init message, starting calibration")
        # launch individual game processes
        
        # pick a random 
        game_no = random.randint(0, 2)
        logger.info(f"Game {game_no} launched")
        if game_no == 1:
            self.calibrate_process = CalibrateInterface()
            self.calibrate_process.run()
        elif game_no == 2:
            self.diode_process = DiodeInterface()
            self.diode_process.run()
        else:
            self.rule_process = RuleInterface()
            self.rule_process.run()

        # 

    def start(self):
        # wait for the turn in signal
        self.message_interface.receive(action_on_data=self.on_message)
