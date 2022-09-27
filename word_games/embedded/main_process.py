
from .game_process import CalibrateInterface, DiodeInterface, RuleInterface
from .interface import MessageInterface
from .utils import logger_config

logger = logger_config()

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
        self.calibrate_process = CalibrateInterface()
        self.calibrate_process.run()
        self.diode_process = DiodeInterface()
        self.diode_process.run()
        self.rule_process = RuleInterface()
        self.rule_process.run()


    def start(self):
        # wait for the turn in signal
        self.message_interface.receive(action_on_data=self.on_message)
