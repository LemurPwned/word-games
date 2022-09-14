import random
from functools import partial

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from rich.console import Console

CRIMSON = (0.8627450980392157, 0.0784313725490196, 0.23529411764705882, 1.0)


class DiodeGameEngine:
    def __init__(self, diodes: int = 6) -> None:
        self.diodes = diodes
        self.console = Console()
        self.print = self.console.print

    def __call__(self):
        self.visualise_game()

    def visualise_game(self):
        def is_game_won():
            for patch in self.patches:
                if patch.get_facecolor() == CRIMSON:
                    return False

            return True

        # generate 6 patches in a row for a matplotlib plot
        self.patches = []
        h = w = 20

        # axs = plt.gridspec.GridSpec(2, self.diodes)
        fig, axs = plt.subplots(2, self.diodes, dpi=300)
        # # Turn off *all* ticks & spines, not just the ones with colormaps.

        for i in range(self.diodes):
            p = random.random()
            color = 'royalblue' if p >= 0.5 else 'crimson'
            patch = mpatches.Rectangle(xy=(0, 0),
                                       width=w,
                                       height=h,
                                       facecolor=color,
                                       edgecolor='0.7')

            self.patches.append(patch)
            axs[0, i].add_artist(patch)
            axs[0, i].set_axis_off()

        def diode_on(val, diode_id):
            for k in (-1, 0, 1):
                indx = (diode_id + k)
                if indx < 0 or indx >= self.diodes:
                    continue
                old_color = self.patches[indx].get_facecolor()
                new_color = 'royalblue' if old_color == CRIMSON else 'crimson'
                self.patches[indx].set_facecolor(new_color)
            fig.canvas.draw_idle()
            if is_game_won():
                self.print("You won!")
                plt.close()

        btns = []
        for i in range(self.diodes):
            bnext = Button(axs[1, i], f'{i}')
            bnext.on_clicked(partial(diode_on, diode_id=i))
            btns.append(
                bnext)  # keep the reference counter for the button alive
        plt.show()

    def ipythonwidgets_visual(self):
        import ipywidgets as ipw

        output = ipw.Output(layout={'border': '1px solid black'})
        with output:
            buttons = [
                ipw.Button(
                    description=f'{i}',
                    layout=ipw.Layout(width='50px', height='50px', color='gray'),
                ) for i in range(self.diodes)
            ]
            colors = [
                'blue' if random.random() > 0.5 else 'red' for _ in range(self.diodes)
            ]
            diodes =  [
                ipw.HTML(
                    f'<div style="background-color: {colors[i]}; width: 50px; height: 50px; border: 1px solid black;"></div>',
                    layout=ipw.Layout(width='50px', height='50px'),
                ) for i in range(self.diodes)
            ]
            def is_game_won():
                for color in colors:
                    if color == 'red':
                        return False
                return True

            def diode_on(b):
                diode_id = int(b.description)
                for k in (-1, 0, 1):
                    indx = (diode_id + k)
                    if indx < 0 or indx >= self.diodes:
                        continue
                    old_color = colors[indx]
                    new_color = 'blue' if old_color == 'red' else 'red'
                    colors[indx] = new_color
                    diodes[
                        indx].value = f'<div style="background-color: {new_color}; width: 50px; height: 50px; border: 1px solid black;"></div>'
                if is_game_won():
                    with output:
                        print("You won!")

            for i in range(self.diodes):
                buttons[i].on_click(diode_on)

            game_box = ipw.VBox([ipw.HBox(diodes), ipw.HBox(buttons), output])
            return game_box


if __name__ == "__main__":
    dg = DiodeGameEngine()
    dg()
