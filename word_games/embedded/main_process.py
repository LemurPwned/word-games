from multiprocessing.dummy import Process
from .game_process import CalibrateInterface, GameInterface, DiodeInterface, RuleInterface
from .utils import logger_config
import random 
import dotenv 
import json
import os
import multiprocessing as mp 
from time import sleep
from queue import Queue
dotenv.load_dotenv()
logger = logger_config()
import uuid
import asyncio
import telegram
from telegram import Bot
from threading import Thread
import playsound

bot = Bot(os.environ["TOKEN"])

async def bot_inform():
    bot = telegram.Bot(os.environ["TOKEN"])
    async with bot:
        print(await bot.send_message())



class Orlowski(GameInterface):
    def __init__(self, port, baud_rate, skip_calibrate = 0)  -> None:
        super().__init__(port, baud_rate=baud_rate)
        self.q = Queue()
        self.skip_calibrate = skip_calibrate # by default no skip
        self.p = Thread(
                target=self.calibration_run, args=(self.queue, ),
            )
        self.current_state = 0 # off

    def on_message(self, message):
        # do something with the message
        # send a message back
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            # logger.error(message)
            return 
        self.current_state = message['init']
        if (self.current_state):
            logger.info("Received init message, starting calibration")
            # launch individual game processes
            self.calibration_run()
        else:
            # print("Maszyna wylaczona")
            ...


    def calibration_run(self):
        br = 9600
        # pick a random 
        game_no = random.randint(0, 2)
        game_names = {
            0: 'Ortopolarnej konsoli kalibracyjnej',
            1: 'Hiperelektronowej konsoli kalibracyjnej',
            2: 'konsoli kalibracyjnej wspolczynnika Weissmana-Ponieckiego'

        }
        logger.info(f"Game {game_no} launched")
        if game_no == 0:
            port = '/dev/ttyACM0'
            process = DiodeInterface(
                port=port, baud_rate=br
            )
        elif game_no == 1:
            port = '/dev/ttyACM2'
            process = RuleInterface(
                port=port, baud_rate=br
            )
        else:
            port = '/dev/ttyACM3'
            process = CalibrateInterface(
                port=port, baud_rate=br
            )
        print(f"Nalezy przeprowadzic kalibracje {game_names[game_no]}")
        self.launch_process(process)


    def launch_process(self, process):
        if not self.skip_calibrate:
            process.run()
        logger.info("The user completed the calibration")
        self.launch_user_console()
        self.message_interface.send(json.dumps({
            'reset': 1
        }))
        print("Zresetuj polozenie klucza w stacyjce startowej do pionu")


    def bot_message_execute(self, msg):
        print("Trwa wysylanie...")
        async def async_bot_send():
            await bot.send_message(chat_id=os.environ["CHAT_ID"], text=msg)
        loop = asyncio.get_event_loop()
        coroutine = async_bot_send()
        loop.run_until_complete(coroutine)

    def launch_user_console(self):
        user_input = input("Wprowadz zasob obliczeniowy. Zaloz zasobowi czepek zaslaniajac uszy i oczy.\nNastepnie wprowadz polecenie i zatwierdz enterem\n")
        self.bot_message_execute(user_input)
        print("Trwa inicjalizowanie. Nie usuwac zasobu obliczeniowego.")
        playsound.playsound("/home/orlowski/word-games/assets/dzwiek_aparatu_orlowskiego.mp3", block=True)
        print(f"Potwierdzenie wyslania polecenia {uuid.uuid4()}.")
        sleep(1)
        print(" Usunac zasob obliczeniowy.")
        sleep(1)
        print("Trwa przetwarzanie. Mozna wprowadzac nastepne polecenia.")
        sleep(0.1)
        return

    def on_init(self):
        print("Zresetuj polozenie klucza w stacyjce startowej do pionu")
        logger.info("Initialisig listening")

