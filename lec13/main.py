import numpy as np
import matplotlib.pyplot as plt

# Константа Кулона (из расчета, что координаты в сантиметрах)
k = 8.988e9

# Границы области визуализации
x_min, x_max = -8, 8
y_min, y_max = -6, 6


def calculate_field(charges, density=500):

    x = np.linspace(x_min, x_max, density)
    y = np.linspace(y_min, y_max, density)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    V = np.zeros_like(X)  # Матрица для потенциала

    for charge in charges:
        x0, y0, q = charge
        dx = X - x0
        dy = Y - y0
        r_squared = dx ** 2 + dy ** 2
        mask = r_squared < 1e-12
        r_squared[mask] = 1e-12
        r = np.sqrt(r_squared)
        E = k * q / r_squared
        Ex += E * dx / r
        Ey += E * dy / r
        V += k * q / r

    return X, Y, Ex, Ey, V


def calculate_force_and_torque(dipole, charges, delta=1e-3):

    x, y, p, alpha = dipole
    alpha_rad = np.deg2rad(alpha)
    px = p * np.cos(alpha_rad)
    py = p * np.sin(alpha_rad)

    def E_field(x_pt, y_pt):
        Ex_total, Ey_total = 0, 0
        for charge in charges:
            x0, y0, q = charge
            dx = x_pt - x0
            dy = y_pt - y0
            r_squared = dx ** 2 + dy ** 2
            if r_squared < 1e-12:
                continue
            r = np.sqrt(r_squared)
            E = k * q / r_squared
            Ex_total += E * dx / r
            Ey_total += E * dy / r
        return Ex_total, Ey_total

    E_x, E_y = E_field(x, y)

    E_x_dx, E_y_dx = E_field(x + delta, y)
    E_x_dy, E_y_dy = E_field(x, y + delta)

    dEx_dx = (E_x_dx - E_x) / delta
    dEx_dy = (E_x_dy - E_x) / delta
    dEy_dx = (E_y_dx - E_y) / delta
    dEy_dy = (E_y_dy - E_y) / delta

    grad_E = np.array([[dEx_dx, dEx_dy],
                       [dEy_dx, dEy_dy]])

    p_vector = np.array([px, py])
    F = grad_E @ p_vector

    tau = px * E_y - py * E_x  # В двумерном случае

    return F, tau, E_x, E_y


def draw_graph(X, Y, Ex, Ey, V, charges, dipoles_info):
    plt.figure(figsize=(10, 8))

    magnitude = np.sqrt(Ex ** 2 + Ey ** 2)
    magnitude[magnitude == 0] = 1e-12
    color = np.log(magnitude)
    strm = plt.streamplot(X, Y, Ex, Ey, color=color, cmap='inferno', linewidth=1, density=2)

    levels = np.linspace(np.min(V), np.max(V), 50)
    contour = plt.contour(X, Y, V, levels=levels, cmap='winter', alpha=0.6)
    plt.clabel(contour, inline=True, fontsize=8, fmt="%.1e")

    for charge in charges:
        x0, y0, q = charge
        if q > 0:
            plt.plot(x0, y0, 'ro', markersize=10, label='Положительный заряд' if charge == charges[0] else "")
        else:
            plt.plot(x0, y0, 'bo', markersize=10, label='Отрицательный заряд' if charge == charges[0] else "")

    for dipole_info in dipoles_info:
        x, y, p, alpha, F, tau = dipole_info
        alpha_rad = np.deg2rad(alpha)
        # Диполь
        dx = p * np.cos(alpha_rad) / 100  # Масштабирование для визуализации
        dy = p * np.sin(alpha_rad) / 100
        plt.arrow(x, y, dx, dy, head_width=0.4, head_length=1, fc='green', ec='green',
                  label='Диполь' if dipole_info == dipoles_info[0] else "")
        # Сила
        Fx, Fy = F
        plt.arrow(x, y, Fx * 1e-12, Fy * 1e-12, head_width=0.2, head_length=0.5, fc='cyan', ec='cyan',
                  label='Сила на диполь' if dipole_info == dipoles_info[0] else "")
        # Момент силы
        plt.plot(x, y, marker=(3, 0, alpha), markersize=12, markerfacecolor='magenta',
                 label='Момент силы' if dipole_info == dipoles_info[0] else "")

    plt.title('Электростатическое поле, эквипотенциальные линии и диполи')
    plt.xlabel('X (см)')
    plt.ylabel('Y (см)')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid(True)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.show()


def main():
    charges = []
    dipoles = []
    dipoles_info = []

    # Ввод зарядов
    n = int(input('Введите количество зарядов: '))
    print('Введите координату x, координату y и величину зарядов через пробел (например: 0 0 1e-9):')
    for i in range(n):
        while True:
            try:
                x, y, q = map(float, input(f'{i + 1}-й заряд: ').split())
                charges.append((x, y, q))
                break
            except ValueError:
                print('Неверный формат. Вводите параметры зарядов в формате [x y q]. Координаты в см, заряд в кулонах.')

    # Ввод диполей
    m = int(input('Введите количество диполей: '))
    if m > 0:
        print(
            'Введите координату x, координату y, модуль дипольного момента и угол направления диполя через пробел (например: 1 1 1e-6 45):')
    for i in range(m):
        while True:
            try:
                x, y, p, alpha = map(float, input(f'{i + 1}-й диполь: ').split())
                dipoles.append((x, y, p, alpha))
                break
            except ValueError:
                print(
                    'Неверный формат. Вводите параметры диполей в формате [x y p alpha]. Координаты в см, p в Кл·см, alpha в градусах.')

    X, Y, Ex, Ey, V = calculate_field(charges)

    for dipole in dipoles:
        F, tau, E_x, E_y = calculate_force_and_torque(dipole, charges)
        x, y, p, alpha = dipole
        dipoles_info.append((x, y, p, alpha, F, tau))
        print(f'\nДиполь в точке ({x}, {y}) см:')
        print(f'  Дипольный момент: {p} Кл·см, угол направления: {alpha}°')
        print(f'  Сила на диполь: Fx = {F[0]:.3e} Н, Fy = {F[1]:.3e} Н')
        print(f'  Момент силы: τ = {tau:.3e} Н·см')

    draw_graph(X, Y, Ex, Ey, V, charges, dipoles_info)


if __name__ == '__main__':
    main()