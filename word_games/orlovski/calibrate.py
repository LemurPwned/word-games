import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from rich.console import Console


class x3DCalibrateEngine:
    def __init__(self, grid_size: int = 25, step_size: int = 1) -> None:
        # generate integer 3D space
        self.grid_size = grid_size
        self.step_size = step_size
        self.space = np.arange(0, grid_size, step_size)
        self.space = np.dstack([self.space for _ in range(3)])
        self.space = self.space.astype(np.int32)
        self.console = Console()
        self.target = [np.random.randint(0, self.grid_size) for _ in range(3)]
        self.pos = [np.random.randint(0, self.grid_size) for _ in range(3)]
        max_distance = self.compute_distance(
            position=[0, 0, 0], target=[grid_size, grid_size, grid_size])
        self.norm = Normalize(vmin=0, vmax=max_distance)
        self.sm = ScalarMappable(norm=self.norm, cmap='inferno')
        self.eps = 6
        self.print = self.console.print

    def compute_distance(self, position, target):
        return np.sqrt(sum([(position[i] - target[i])**2 for i in range(3)]))

    def __call__(self) -> None:
        self.print(f"Generating seed for grid size: {self.grid_size}")
        self.print(f"Step size: {self.step_size}")
        self.visualise_3D_space()

    def is_game_won(self):
        if self.compute_distance(self.pos, self.target) < self.eps:
            return True
        return False

    def visualise_3D_space(self) -> None:
        fig, ax = plt.subplots()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        graph = ax.scatter3D(*self.pos, color="royalblue", s=10)
        _ = ax.scatter3D(*self.target, color="crimson", s=20)
        ax.set_xlim(0, 30)
        ax.set_ylim(0, 30)
        ax.set_zlim(0, 30)
        ax.set_axis_off()
        # adjust the main plot to make room for the sliders
        pi = np.pi
        cos = np.cos
        sin = np.sin
        phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0 * pi:100j]
        # draw epsilon ball
        x = self.eps * sin(phi) * cos(theta) + self.target[0]
        y = self.eps * sin(phi) * sin(theta) + self.target[1]
        z = self.eps * cos(phi) + self.target[2]
        ax.plot_surface(x,
                        y,
                        z,
                        rstride=2,
                        cstride=2,
                        color='c',
                        alpha=0.1,
                        linewidth=0.1)
        ax.axis('off')
        fig.subplots_adjust(left=0.25, bottom=0.45)

        # Make a horizontal slider to control the frequency.
        ax_xpot = plt.axes([0.25, 0.1, 0.65, 0.03])
        ax_ypot = plt.axes([0.25, 0.2, 0.65, 0.03])
        ax_zpot = plt.axes([0.25, 0.3, 0.65, 0.03])

        ax_indicator = plt.axes([0.05, 0.3, 0.1, 0.1])
        ax_indicator.axis('off')

        rect = mpatches.Rectangle([0, 0], width=10, height=10)
        ax_indicator.add_artist(rect)
        dist = self.compute_distance(self.pos, self.target)
        rect.set_facecolor(self.sm.to_rgba(dist))
        x_slider = Slider(
            ax=ax_xpot,
            label='X',
            valmin=0.,
            valmax=30,
            valinit=self.pos[0],
        )
        y_slider = Slider(
            ax=ax_ypot,
            label='Y',
            valmin=0.1,
            valmax=30,
            valinit=self.pos[1],
        )
        z_slider = Slider(
            ax=ax_zpot,
            label='Z',
            valmin=0.1,
            valmax=30,
            valinit=self.pos[2],
        )

        # The function to be called anytime a slider's value changes
        def update(val):
            self.pos = (x_slider.val, y_slider.val, z_slider.val)
            if self.is_game_won():
                self.print("Game won!")
            dist = self.compute_distance(self.pos, self.target)
            rect.set_facecolor(self.sm.to_rgba(dist))
            graph._offsets3d = ([x_slider.val], [y_slider.val], [z_slider.val])
            fig.canvas.draw_idle()

        # register the update function with each slider
        for slider in (x_slider, y_slider, z_slider):
            slider.on_changed(update)

        # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
        resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', hovercolor='0.975')

        def reset(event):
            for slider in (x_slider, y_slider, z_slider):
                slider.reset()

        button.on_clicked(reset)
        plt.show()


if __name__ == "__main__":
    engine = x3DCalibrateEngine(30, 1)
    engine()