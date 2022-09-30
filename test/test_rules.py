from word_games.embedded.game_process import CalibrateInterface, RuleInterface
from word_games.embedded.interface import MessageInterface
import json

if __name__ == "__main__":
    port = '/dev/ttyACM0'
    br = 9600
    interface = RuleInterface(
        port=port, baud_rate=br
    )
    interface.run()