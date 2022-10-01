from word_games.embedded.game_process import CalibrateInterface

if __name__ == "__main__":
    port = '/dev/ttyACM3'
    br = 9600
    interface = CalibrateInterface(
        port=port, baud_rate=br
    )
    interface.run()
