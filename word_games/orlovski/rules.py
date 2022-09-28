import math
import random


class Rule:
    def __init__(self, name: str, rule: str, num_false: int = 2) -> None:
        self.name = name
        self.rule = rule
        self.num_false = num_false
        self.description = f'{name}: {rule}'

    def __call__(self) -> int:
        # generate only one true answer
        lst = [self.generate_true(),
        *[self.generate_false() for _ in range(self.num_false)]]
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
        return max(num - num % 3, 3)

    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 3 == 0:
            return num + 1
        return num

class DivisibleBy5Rule(Rule):
    def generate_true(self):
        num = random.randint(0, 9999)
        return max(num - num%5, 5)

    def generate_false(self):
        num = random.randint(0, 9999)
        if num % 5 == 0:
            return num + 1
        return num


class PowerOf2Rule(Rule):
    all_powers = [
        2 ** i for i in range(0, 14)
    ]
    def generate_true(self):
        # max 4-digit power of 2 is 2^13 = 8192
        num = random.randint(0, 13)
        return self.all_powers[num]

    def generate_false(self):
        num = random.randint(0, 9999)
        if num in self.all_powers:
            return num + 1
        return num


class RuleGameEngine():
    def __init__(self, score_to_collect = 5) -> None:
        self.ruleset = [EvenRule('Even', 'is even'),
                OddRule('Odd', 'is odd'),
                DivisibleBy3Rule('Divisible by 3', 'is divisible by 3'),
                DivisibleBy5Rule('Divisible by 5', 'is divisible by 5'),
                PowerOf2Rule('Power of 2', 'is power of 2')]
        self.current_rule = random.choice(self.ruleset)
        self.current_rule = self.ruleset[0]
        self.score = 0
        self.to_collect = score_to_collect

    def ipythonwidgets_visual(self):
        import ipywidgets as ipw


        out = ipw.Output()
        score_tab = ipw.HTML(value=f'<div>Score: {self.score}/{self.to_collect}</div>')
        lst, self.current_correct_ans = self.current_rule()
        buttons = [ipw.Button(description=str(i)) for i in lst]

        def on_button_clicked(b):
            if int(b.description) == self.current_correct_ans:
                self.score += 1
                score_tab.value = f'<div>Score: {self.score}/{self.to_collect}</div>'
            else:
                self.score -= 1
                score_tab.value = f'<div>Score: {self.score}/{self.to_collect}</div>'

            if self.score == self.to_collect:
                self.score = 0
                with out:
                    print("You won!")

            lst, self.current_correct_ans = self.current_rule()
            for i, but in enumerate(buttons):
                but.description = str(lst[i])

        for i, button in enumerate(buttons):
            button.on_click(on_button_clicked)

        return ipw.VBox([score_tab, ipw.HBox(buttons), out])
