from word_games.embedded.main_process import Orlowski
if __name__ == "__main__":
    port = '/dev/ttyACM0'
    br = 9600
    interface = Orlowski(
        port=port, baud_rate=br
    )
    interface.run()
 