from word_games.embedded.game_process import DiodeInterface

if __name__ == "__main__":
    port = '/dev/ttyACM0'
    br = 9600
    interface = DiodeInterface(
        port=port, baud_rate=br
    )
    interface.run()
 