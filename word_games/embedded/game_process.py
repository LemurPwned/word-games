from curses import baudrate
import json
import math
import random

import numpy as np

from ..orlovski.rules import DivisibleBy5Rule, EvenRule, OddRule, PowerOf2Rule
from .interface import MessageInterface
from .utils import logger_config

logger = logger_config()

class GameInterface:
    def __init__(self, port, baud_rate=115200) -> None:
        self.message_interface = MessageInterface(port=port,
            baud_rate=baud_rate,
            read_interval=0.1)

    def run(self):
        self.on_init()
        logger.info("Listening...")
        self.message_interface.receive(action_on_message=self.on_message)

    def on_init(self):
        raise NotImplementedError

    def on_win(self):
        raise NotImplementedError

    def on_message(self, message):
        raise NotImplementedError

class CalibrateInterface(GameInterface):
    def __init__(self, port, baud_rate, grid_size= 30, step_size=  0.5, eps=5) -> None:
        super().__init__(port, baud_rate=baud_rate)
        self.eps = eps
        self.max_distance = self.compute_distance(
            position=[0, 0, 0], target=[grid_size, grid_size, grid_size])
        self.min_distance = self.eps
        self.grid_size = grid_size
        self.step_size = step_size

    def on_init(self):
        self.generate_target_position()
        self.message_interface.send(json.dumps({
            # "target": self.target.tolist(),
            # "position": self.initial_position.tolist(),
            "win": False,
            "progress": self.compute_distance(self.initial_position, self.target)
        }))

    def on_win(self):
        logger.info("Game won"  )

    def generate_target_position(self):
        min_distance = self.grid_size
        max_distance = self.grid_size**2
        distance = np.random.randint(min_distance, max_distance)
        # generate a target
        self.target = [np.random.randint(0, self.grid_size) for _ in range(3)]
        x = np.random.randint(0, self.grid_size)
        y = np.random.randint(0, self.grid_size)
        def inverted_distance(d, pos):
            # d^2 = x^2 + y^2 + z^2
            # z^2 = d^2 - x^2 - y^2
            # z = sqrt(d^2 - x^2 - y^2)
            return math.sqrt(d**2 - pos[0]**2 - pos[1]**2)
        z = inverted_distance(distance, [x, y])
        self.initial_position = [x, y, z]

    def on_message(self, message):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            return
        (x, y, z) = message['position']
        pos = (x*self.grid_size*1.2, y*self.grid_size*1.2, z*self.grid_size)
        distance = self.compute_distance(pos, self.target)
        # print(self.target, pos, self.eps, distance)
        if distance <= self.eps:
            self.message_interface.send(json.dumps({
                "win": True,
                "progress":  100,
                # "postion": pos,
                # "target": self.target
            }))
            self.on_win()
        else:
            self.message_interface.send(json.dumps({
                "win": False,
                "progress": self.progress_bar(distance),
                # "position": pos,
                # "target": self.target

            }))

    def compute_distance(self, position, target):
        return math.sqrt(sum([(position[i] - target[i])**2 for i in range(3)]))


    def progress_bar(self, dst):
        # normalise distance
        dst = (dst - self.min_distance) / (self.max_distance - self.min_distance)
        val = min(max(1 - dst, 0), 1)*100.
        print(val)
        return val




class DiodeInterface(GameInterface):
    def __init__(self, port, baud_rate, diodes=6, bias=0.35) -> None:
        super().__init__(port, baud_rate=baud_rate)
        self.diodes = diodes
        self.prev_buttons = [0 for _ in range(self.diodes)]
        self.current_buttons = []
        self.bias = bias

    def on_win(self):
        logger.debug("WINN")
        self.message_interface.send(json.dumps(
            {
                "win": True,
                "diodes": self.diodes
            }
        ))

    def generate_diode_states(self):
        diode_states = []
        for _ in range(self.diodes):
            p = random.random()
            if p < self.bias:
                diode_states.append(True)
            else:
                diode_states.append(False)
        return diode_states

    def on_init(self):
        self.diode_states = self.generate_diode_states()
        while all(self.diode_states):
            self.diode_states = self.generate_diode_states()

        self.message_interface.send(json.dumps(
            {
                "win": False,
                "diodes": self.diode_states
            }
        ))

    def on_message(self, message):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            return
        btn_states = message['buttons']
        changed_diode_id = None
        for i, btn in enumerate(btn_states):
            if btn != self.prev_buttons[i]:
                changed_diode_id = i
        if not (changed_diode_id is None):
            self.prev_buttons = btn_states
            for k in (-1, 0, 1):
                diode_id = changed_diode_id + k
                if diode_id > 0 and diode_id < len(self.diode_states):
                    self.diode_states[diode_id] = (not self.diode_states[diode_id])
        logger.debug(f"DIODE STATES {self.diode_states}")
        if not any(self.diode_states):
            self.on_win()
        else:
            # change diodes adequately
            self.message_interface.send(json.dumps(
                {
                    "win": False,
                    "diodes": self.diode_states
                }
            ))


class RuleInterface(GameInterface):
    def __init__(self, port, baud_rate) -> None:
        super().__init__(port, baud_rate=baud_rate)
        self.score = 0
        self.min_score = 15
        self.max_attempts = 30
        self.attempts = 0


    def on_init(self):
        # initialise Rule
        self.current_rule = random.choice(
            (EvenRule(), OddRule(), DivisibleBy5Rule())
        )
        self.lst, self.correct = self.current_rule()
        self.message_interface.send(json.dumps(
            {
                "win": False,
                "numbers": self.lst,
                "score": self.score
            }
        ))

    def on_win(self):
        self.message_interface.send(json.dumps(
            {
                "win": True,
                "numbers": self.lst,
                "score": self.score
            }
        ))


    def on_message(self, message):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            return
        answ = self.lst[message['ans']]
        self.attempts += 1
        if answ == self.correct:
            self.score += 1
        if self.score >= self.min_score:
            self.on_win()
        elif self.attempts >= self.max_attempts:
            self.on_win()
        else:
            self.lst, self.correct = self.current_rule()
            self.message_interface.send(json.dumps(
                {
                    "win": False,
                    "numbers": self.lst,
                    "score": self.score
                }
            ))
