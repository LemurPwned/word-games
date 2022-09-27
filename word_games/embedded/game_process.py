import json
import math
import random
from asyncio.log import logger

import numpy as np

from ..orlovski.rules import DivisibleBy5Rule, EvenRule, OddRule
from .interface import MessageInterface
from .utils import logger_config

logger = logger_config()

class GameInterface:
    def __init__(self) -> None:
        self.message_interface = MessageInterface(port="/dev/ttyUSB0",
        baud_rate=9600,
        read_interval=0.05)

    def run(self):
        self.on_init()
        self.message_interface.receive(action_on_data=self.on_message)

    def on_init(self):
        raise NotImplementedError

    def on_win(self):
        raise NotImplementedError

    def on_message(self, message):
        raise NotImplementedError

class CalibrateInterface(GameInterface):
    def __init__(self, grid_size= 30, step_size=  0.5, eps=0.1) -> None:
        super().__init__()
        self.eps = eps
        self.max_distance = self.compute_distance(
            position=[0, 0, 0], target=[grid_size, grid_size, grid_size])
        self.min_distance = self.eps
        self.grid_size = grid_size
        self.step_size = step_size

    def on_init(self):
        self.generate_target_position()
        self.message_interface.send(json.dumps({
            "target": self.target.tolist(),
            "position": self.initial_position.tolist(),
            "win": False,
            "progress": self.compute_distance(self.initial_position, self.target)
        }))

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
        message = json.loads(message)
        (x, y, z) = message['position']
        pos = (x, y, z)
        distance = self.compute_distance(pos, self.target)
        if distance <= self.eps:
            self.message_interface.send(json.dumps({
                "win": True,
                "progress": 1,
                "postion": pos,
                "target": self.target
            }))
            self.on_win()
        else:
            self.message_interface.send(json.dumps({
                "win": False,
                "progress": self.progress_bar(distance),
                "position": pos,
                "target": self.target

            }))

    def compute_distance(self, position, target):
        return math.sqrt(sum([(position[i] - target[i])**2 for i in range(3)]))


    def progress_bar(self, dst):
        # normalise distance
        dst = (dst - self.min_distance) / (self.max_distance - self.min_distance)
        return min(max(1 - dst, 0), 1)




class DiodeInterface(GameInterface):
    def __init__(self, diodes, bias) -> None:
        super().__init__()
        self.diodes = diodes
        self.bias = 0.35

    def on_win(self):
        ...

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

        diode_states = self.generate_diode_states()
        while all(diode_states):
            diode_states = self.generate_diode_states()

        self.message_interface.send(json.dumps(
            {
                "win": False,
                "diodes": diode_states
            }
        ))

    def on_message(self, message):
        message = json.loads(message)
        diode_states = message['diodes']
        changed_diode_id = message['changed_diode']
        for k in (-1, 0, 1):
            diode_id = changed_diode_id + k
            if diode_id > 0 and diode_id < len(diode_states):
                diode_states[diode_id] = (not diode_states[diode_id])

        if all(diode_states):
            self.message_interface.send(json.dumps(
                {
                    "win": True,
                    "diodes": diode_states
                }
            ))
            self.on_win()
        else:
            # change diodes adequately
            self.message_interface.send(json.dumps(
                {
                    "win": False,
                    "diodes": diode_states
                }
            ))


class RuleInferface:
    def __init__(self) -> None:
        self.score = 0

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
                "correct": self.correct,
                "score": self.score
            }
        ))


    def on_message(self, message):
        message = json.loads(message)
        answ = message['answer']
        if answ == self.correct:
            self.score += 1
        if self.score >= 10:
            self.on_win()
        else:
            self.lst, self.correct = self.current_rule()
            self.message_interface.send(json.dumps(
                {
                    "win": False,
                    "numbers": self.lst,
                    "correct": self.correct,
                    "score": self.score
                }
            ))
