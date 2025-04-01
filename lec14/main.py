import numpy as np
import matplotlib.pyplot as plt


# Найти E2 и theta2
def solve_refraction_angles(eps1, eps2, E, theta1_deg):

    theta1 = np.radians(theta1_deg)

    theta2 = np.arctan((eps2 * np.sin(theta1)) / (eps1 * np.cos(theta1)))
    theta2_deg = np.degrees(theta2)

    sin_t1 = np.sin(theta1)
    sin_t2 = np.sin(theta2)
    if abs(sin_t2) < 1e-14:
        E2 = 0.0
    else:
        E2 = E * (sin_t1 / sin_t2)

    return E2, theta2_deg


# Вспомогательная функция для calculate_for_graphs()
def field_E(E1, E2, x, y, angle1, angle2):
        if y > 0:
            Ex = E1 * np.sin(angle1)
            Ey = E1 * np.cos(angle1)
        else:
            Ex = E2 * np.sin(angle2)
            Ey = E2 * np.cos(angle2)
        return Ex, Ey


# Считает данные необходимые для отображения графика
def calculate_for_graphs(E, E2, theta1_deg, theta2_deg):
    angle1 = np.radians(theta1_deg)
    angle2 = np.radians(theta2_deg)

    x_min, x_max = -2.0, 2.0
    y_min, y_max = -2.0, 2.0

    nx, ny = 200, 200  # разрешение
    x_vals = np.linspace(x_min, x_max, nx)
    y_vals = np.linspace(y_min, y_max, ny)
    X, Y = np.meshgrid(x_vals, y_vals)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for i in range(ny):
        for j in range(nx):
            Ex[i, j], Ey[i, j] = field_E(E, E2, X[i, j], Y[i, j], angle1, angle2)

    return X, Y, Ex, Ey


# Построение графика
def draw_graph(X, Y, Ex, Ey):
    fig, ax = plt.subplots(figsize=(7, 7))
    stream = ax.streamplot(X, Y, Ex, Ey,
                         density=1.2,
                         linewidth=1,
                         arrowsize=1,
                         color=np.hypot(Ex, Ey),
                         cmap='plasma')

    cb = fig.colorbar(stream.lines, ax=ax, orientation='vertical')
    cb.set_label('Величина поля |E|')

    ax.axhline(0, color='k', linewidth=2)
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.tight_layout()
    plt.show()


def main():
    eps1 = float(input("Диэлектрическую проницаемость среды 1: "))
    eps2 = float(input("Диэлектрическую проницаемость среды 2: "))
    E = float(input("Модуль напряженности E: "))
    theta1_deg = float(input("Введите угол падения в градусах: "))

    E2, theta2_deg = solve_refraction_angles(eps1, eps2, E, theta1_deg)

    print(f"Среда 1: E = {E:.3f}, theta = {theta1_deg:.1f} градусов")
    print(f"Среда 2: E = {E2:.3f}, theta = {theta2_deg:.1f} градусов")

    X, Y, Ex, Ey = calculate_for_graphs(E, E2, theta1_deg, theta2_deg)

    draw_graph(X, Y, Ex, Ey)


if __name__ == "__main__":
    main()
