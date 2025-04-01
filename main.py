import numpy as np
import matplotlib.pyplot as plt

# const
g = 9.81

def calculate(initial_height, initial_velocity, launch_angle):
    angle_rad = np.radians(launch_angle)

    t_flight = (initial_velocity * np.sin(angle_rad) + np.sqrt((initial_velocity * np.sin(angle_rad)) ** 2 + 2 * g * initial_height)) / g

    t = np.linspace(0, t_flight, num=500)

    x = initial_velocity * np.cos(angle_rad) * t
    y = initial_height + initial_velocity * np.sin(angle_rad) * t - 0.5 * g * t**2

    return t, x, y

def draw_graphs(t, x, y, initial_velocity, launch_angle):
    plt.figure(figsize=(10, 6))

    # Trajectory (x / y)
    plt.subplot(2, 1, 1)
    plt.plot(x, y)
    plt.title('Траектория движения')
    plt.xlabel('Ox (м)')
    plt.ylabel('Oy (м)')
    plt.grid()

    # Speed / time
    plt.subplot(2, 2, 3)
    velocity_x = initial_velocity * np.cos(np.radians(launch_angle)) * np.ones_like(t)
    velocity_y = initial_velocity * np.sin(np.radians(launch_angle)) - g * t
    speed = np.sqrt(velocity_x**2 + velocity_y**2)
    plt.plot(t, speed)
    plt.title('Скорость / времени')
    plt.xlabel('t (с)')
    plt.ylabel('V (м/с)')
    plt.grid()

    # Coordinates (x, y) / time
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
    launch_angle = float(input("Угол (градусы): "))
    initial_velocity = float(input("Начальная скорость (м/с): "))
    initial_height = float(input("Начальная высоту (м): "))

    t, x, y = calculate(initial_height, initial_velocity, launch_angle)

    draw_graphs(t, x, y, initial_velocity, launch_angle)

if __name__ == "__main__":
    main()