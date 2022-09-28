import time
from multiprocessing import Queue

import serial


class MessageInterface:
    """Base class for message interface"""
    def __init__(self, port: str, baud_rate: int = 9600, read_interval: float = 0.05,  shared_queue: Queue = None) -> None:
        """
        Initialize serial port and queue
        :param port: serial port
        :param baud_rate: baud rate
        :param read_interval: interval between reading from serial port
        :param shared_queue: queue to put messages in [default None, creates new queue]
        """
        self.port = port
        self.baud_rate = baud_rate
        self.read_interval = read_interval
        self.serial = serial.Serial(port=port, baudrate=baud_rate, write_timeout=0.1,  timeout=0.1)
        if shared_queue is None:
            self.shared_queue = Queue()
        else:
            if not isinstance(shared_queue, Queue):
                raise TypeError("shared_queue must be a multiprocessing.Queue")
            self.shared_queue = shared_queue

    def receive(self, action_on_message=None):
        """
        Read from serial port and put messages in queue
        """
        while True:
            data = self.serial.readline()
            time.sleep(self.read_interval)
            if data:
                action_on_message(data)
                # self.shared_queue.put(data)


    def send(self, message):
        """
        Send message to serial port
        """
        self.serial.write(message)
