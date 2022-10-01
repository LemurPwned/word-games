from word_games.embedded.main_process import Orlowski
import sys 

if __name__ == "__main__":
    try:
        skip_calibrate = sys.argv[1]
    except IndexError:
        skip_calibrate = 0
    port = '/dev/ttyACM1'
    br = 9600
    interface = Orlowski(
        port=port, baud_rate=br, skip_calibrate=skip_calibrate
    )
    interface.run()
 