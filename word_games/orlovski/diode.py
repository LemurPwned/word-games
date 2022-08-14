import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from functools import partial
from rich.console import Console
import random

CRIMSON = (0.8627450980392157, 0.0784313725490196, 0.23529411764705882, 1.0)


class DiodeGameEngine:
    def __init__(self, diodes: int = 6) -> None:
        self.diodes = diodes
        self.console = Console()
        self.print = self.console.print

    def __call__(self):
        self.visualise_game()

    def visualise_game(self):
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
            for k in (-1, 1):
                indx = (diode_id + k)
                if indx < 0 or indx >= self.diodes:
                    continue
                old_color = self.patches[indx].get_facecolor()
                new_color = 'royalblue' if old_color == CRIMSON else 'crimson'
                self.patches[indx].set_facecolor(new_color)
            fig.canvas.draw_idle()
            if self.is_game_won():
                self.print("You won!")
                plt.close()

        btns = []
        for i in range(self.diodes):
            bnext = Button(axs[1, i], f'{i}')
            bnext.on_clicked(partial(diode_on, diode_id=i))
            btns.append(
                bnext)  # keep the reference counter for the button alive
        plt.show()

    def is_game_won(self):
        for patch in self.patches:
            if patch.get_facecolor() == CRIMSON:
                return False

        return True


if __name__ == "__main__":
    dg = DiodeGameEngine()
    dg()