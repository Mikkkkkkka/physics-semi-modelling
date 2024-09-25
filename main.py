import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def calculate(r: float):
    t = np.linspace(0, 1000, 2000)
    x = r * (t - np.sin(t))
    y = r * (1 - np.cos(t))
    return t, x, y

def draw_graph(t, x, y, r, velocity):
    figure, axis, = plt.subplots()
    traj = axis.plot(x[0], y[0])[0]
    axis.set(xlim=(0, 30), ylim=(-10, 10))
    plt.grid()

    def update(frame):
        traj.set_xdata(x[:frame])
        traj.set_ydata(y[:frame])
        return traj,

    anim = FuncAnimation(fig=figure, func=update, frames=60, interval=50 - (velocity / r))
    plt.show()


if __name__ == '__main__':
    radius = float(input('Радиус (м): '))
    speed = float(input('Скорость центра (м/с): '))

    outer_t, outer_x, outer_y = calculate(radius)
    draw_graph(outer_t, outer_x, outer_y, radius, speed)
