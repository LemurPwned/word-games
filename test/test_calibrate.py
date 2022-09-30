from word_games.embedded.game_process import CalibrateInterface, RuleInferface
from word_games.embedded.interface import MessageInterface

if __name__ == "__main__":
    port = '/dev/ttyACM2'
    br = 9600
    interface = CalibrateInterface(
        port=port, baud_rate=br
    )
    interface.run()
 