import random

from rich.panel import Panel
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, ButtonPressed, Static
from rich.panel import Panel
import sys 
import rich.box
class Rule:
    def __init__(self, name: str, rule: str, num_false: int = 2) -> None:
        self.name = name
        self.rule = rule
        self.num_false = num_false
        self.description = f'{name}: {rule}'
    
    def __call__(self) -> int:
        # generate only one true answer 
        lst = [self.generate_true(), *[self.generate_false() for _ in range(self.num_false)]]
        correct_ans = lst[0]
        random.shuffle(lst)
        return lst, correct_ans

class EvenRule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num % 2 == 0:
            return num
        return num + 1

    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 2 == 0:
            return num + 1
        return num 

class OddRule(Rule):
    def generate_true(self):
        """Generate 4 digit odd number"""
        num = random.randint(0, 9999)
        if num % 2 == 0:
            num += 1
        return num
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 2 == 0:
            num -= 1
        return num

class DivisibleBy3Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num % 3 == 0:
            return num
        return num + 1
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 3 == 0:
            return num + 1
        return num

class DivisibleBy5Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num % 5 == 0:
            return num
        return num + 1
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 5 == 0:
            return num + 1
        return num

class DivisibleBy7Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num % 7 == 0:
            return num
        return num + 1
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 7 == 0:
            return num + 1
        return num

class DivisibleBy11Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num % 11 == 0:
            return num
        return num + 1
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 11 == 0:
            return num + 1
        return num

class PowerOf2Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num & (num - 1) == 0:
            return num
        return num + 1
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num & (num - 1) == 0:
            return num + 1
        return num

class PowerOf3Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        if num & (num - 1) == 0:
            return num
        return num + 1
    
    def generate_false(self):
        num = random.randint(0, 9999)
        if num & (num - 1) == 0:
            return num + 1
        return num

class Hover(Widget):

    mouse_over = Reactive(False)
    def set_text(self, text: str) -> None:
        self.text = text

    def render(self) -> Panel:
        return Panel(self.text, style=("on red" if self.mouse_over else ""))

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

    


class RulesEngine(App):
    DARK = "white on rgb(51,51,51)"
    LIGHT = "black on rgb(165,165,165)"
    YELLOW = "white on rgb(255,159,7)"


    a = Reactive("a")
    b = Reactive("b")
    c = Reactive("c")

    def __init__(self,
                 screen: bool = True,
                 driver_class: None = None,
                 log: str = "",
                 log_verbosity: int = 1,
                 title: str = "Rule Games"):
        super().__init__(screen, driver_class, log, log_verbosity, title)
        self.ruleset = [EvenRule('Even', 'is even'), 
        OddRule('Odd', 'is odd'), 
        DivisibleBy3Rule('Divisible by 3', 'is divisible by 3'), 
        DivisibleBy5Rule('Divisible by 5', 'is divisible by 5'), 
        DivisibleBy7Rule('Divisible by 7', 'is divisible by 7'), 
        DivisibleBy11Rule('Divisible by 11', 'is divisible by 11'), 
        PowerOf2Rule('Power of 2', 'is power of 2'), 
        PowerOf3Rule('Power of 3', 'is power of 3')]

        self.current_rule = self.ruleset[0]
        self.score = 0 
        self.to_collect = 5


    def make_button(self, text: str, style: str) -> Button:
            """Create a button with the given Figlet label."""
            return Button(text, style=style, name=text)

    def update_btns(self, lst):
        self.a = Button(str(lst[0]))
        self.b = Button(str(lst[1]))
        self.c = Button(str(lst[2]))

    async def on_mount(self) -> None:
        lst, self.current_correct_ans = self.current_rule()
        self.update_btns(lst)
        await self.mount_widgets()


    async def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the button widget"""
        assert isinstance(message.sender, Button)
        button_name = message.sender.name
        print("Pressed button:", button_name)
        if button_name == str(self.current_correct_ans):
            self.score += 1 
        else:
            self.score -= 1
        if self.score == self.to_collect:
            # reset 
            print("You win")
            sys.exit()
        elif self.score < -self.to_collect:
            print("You lose")
            sys.exit()
        else:
            # generate new set of numbers
            self.view.layout.docks.clear()
            lst, self.current_correct_ans = self.current_rule()
            self.update_btns(lst)
            await self.mount_widgets()

    async def mount_widgets(self):
        await self.view.dock(Static(renderable=Panel(
            f"## {self.score}/{self.to_collect}", title="Score", border_style='yellow', box=rich.box.ROUNDED)), size=3)
        await self.view.dock(*(self.a, self.b, self.c), edge="bottom")

    async def clear_screen(self) -> None:
        self.view.layout.docks.clear()
        self.view.widgets.clear()


if __name__ == "__main__":
    RulesEngine.run(log="textual.log")
