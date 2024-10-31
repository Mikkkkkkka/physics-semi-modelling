import numpy as np
import matplotlib.pyplot as plt

# Константы
g = 9.81


def calculate(initial_height, initial_velocity, launch_angle, air_resistance):
    angle_rad = np.radians(launch_angle)
    delta_t = 0.01
    t_flight = (initial_velocity * np.sin(angle_rad) + np.sqrt((initial_velocity * np.sin(angle_rad)) ** 2 + 2 * g * initial_height)) / g
    # Предполагаемое время полёта, реальное будет меньше

    # Начальные условия
    x = [0]
    y = [0]
    v_x = initial_velocity * np.cos(angle_rad)
    v_y = initial_velocity * np.sin(angle_rad)

    # Итеративный рассчёт координат
    while True:
        f_g = -g
        f_d = -air_resistance * np.sqrt(v_x ** 2 + v_y ** 2)

        a_x = f_d * (v_x / np.sqrt(v_x ** 2 + v_y ** 2))
        a_y = f_g + f_d * (v_y / np.sqrt(v_x ** 2 + v_y ** 2))

        v_x += a_x * delta_t
        v_y += a_y * delta_t

        x.append(x[-1] + v_x * delta_t)
        y.append(y[-1] + v_y * delta_t)

        if y[-1] < 0:
            break

    x = x[:-1]
    y = y[:-1]
    t = np.linspace(0, len(x) * delta_t, len(x))
    return t, np.array(x), np.array(y)


def draw_graphs(t, x, y):
    plt.figure(figsize=(10, 6))

    # Траектория (x / y)
    plt.subplot(2, 1, 1)
    plt.plot(x, y)
    plt.title('Траектория движения')
    plt.xlabel('Ox (м)')
    plt.ylabel('Oy (м)')
    plt.grid()

    # Скорость / время
    plt.subplot(2, 2, 3)
    velocity_x = (np.diff(x) / np.diff(t))
    velocity_y = (np.diff(y) / np.diff(t))
    total_velocity = np.sqrt(velocity_x**2 + velocity_y**2)
    plt.plot(t[:-1], total_velocity)
    plt.title('Скорость / время')
    plt.xlabel('t (с)')
    plt.ylabel('v (м/с)')
    plt.grid()

    # Координаты (x, y) / время
    plt.subplot(2, 2, 4)
    plt.plot(t, x, label='x')
    plt.plot(t, y, label='y')
    plt.title('Координаты / время')
    plt.xlabel('t (с)')
    plt.ylabel('x/y (м)')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


def main():
    launch_velocity = float(input("Начальная скорость (м/с): "))
    launch_angle = float(input("Угол (градусы): "))
    launch_height = float(input("Начальная высота (м): "))
    k = float(input("Коэффициент сопротивления (k): "))

    t, x, y = calculate(launch_height, launch_velocity, launch_angle, k)

    draw_graphs(t, x, y)


if __name__ == "__main__":
    main()