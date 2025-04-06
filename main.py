import numpy as np
import matplotlib.pyplot as plt

m = 3.0
R = 3.0
alpha = 5 * np.pi / 6
mu = 0.04
g = 9.81

def calculate():
    v0_min = np.sqrt(5 * g * R)

    v0 = v0_min

    h = R * (1 - np.cos(alpha))

    W_fric = mu * m * g * R * abs(np.sin(alpha) - np.sin(0))

    E_kyn_0 = 0.5 * m * v0 ** 2
    E_pot = m * g * h
    E_kyn_alpha = E_kyn_0 - E_pot - W_fric
    v_alpha = np.sqrt(2 * E_kyn_alpha / m)

    theta = np.linspace(0, alpha, 500)

    x_arc = R * np.sin(theta)
    y_arc = -R * np.cos(theta) + R

    phi = theta[-1] + np.pi / 2

    v_x = v_alpha * np.cos(phi)
    v_y = v_alpha * np.sin(phi)
    # Костыль
    if alpha > np.pi:
        v_x *= -1

    t = np.linspace(0, 1, 100)

    x_fall = x_arc[-1] + v_x * t
    y_fall = y_arc[-1] + v_y * t + -0.5 * g * t ** 2

    return v0_min, x_arc, y_arc, x_fall, y_fall,


def draw_graph(x_arc, y_arc, x_fall, y_fall):
    plt.figure(figsize=(10, 6))

    plt.title('Траектория движения тела по дуге и после схода с дуги')
    plt.plot(x_arc, y_arc, label='Движение по дуге')
    plt.plot(x_fall, y_fall, label='Движение после схода с дуги', linestyle='--')
    plt.xlabel('X, м')
    plt.ylabel('Y, м')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')

    plt.show()

def main():
    v0_min, x_arc, y_arc, x_fall, y_fall = calculate()

    print(f"Минимальная начальная скорость для сохранения контакта v0_min = {v0_min:.2f} м/с")

    draw_graph(x_arc, y_arc, x_fall, y_fall)

if __name__ == '__main__':
    main()