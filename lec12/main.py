import numpy as np
import matplotlib.pyplot as plt

# Константа Кулона (из расчета, что координаты в сантиметрах)
k = 8.988e9

# Границы области визуализации
x_min, x_max = -8, 8
y_min, y_max = -6, 6

def calculate(charges):
    density = 500  # Плотность сетки
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

def draw_graph(X, Y, Ex, Ey, V, charges):
    plt.figure(figsize=(8, 6))

    # Электростатическое поле
    color = np.log(np.sqrt(Ex ** 2 + Ey ** 2))  # Цвет по модулю поля
    plt.streamplot(X, Y, Ex, Ey, color=color, cmap='inferno', linewidth=1, density=2)

    # Эквипотенциальные линии
    levels = np.linspace(np.min(V), np.max(V), 50)  # Количество уровней потенциала
    contour = plt.contour(X, Y, V, levels=levels, cmap='winter', alpha=0.6)
    plt.clabel(contour, inline=True, fontsize=8, fmt="%.1e")

    # Отображение зарядов
    for charge in charges:
        x0, y0, q = charge
        if q > 0:
            plt.plot(x0, y0, 'ro', markersize=10)
        else:
            plt.plot(x0, y0, 'bo', markersize=10)

    plt.title('Электростатическое поле и эквипотенциальные линии системы точечных зарядов')
    plt.xlabel('X (см)')
    plt.ylabel('Y (см)')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid(True)
    plt.show()

def main():
    charges = []
    n = int(input('Введите количество зарядов: '))
    print(f'Введите координату x, координату y и величину зарядов в виде через пробел.')

    while True:
        try:
            for i in range(n):
                (x, y, q) = map(float, input(f'{i + 1}-й заряд: ').split())
                charges.append((x, y, q))
            break
        except ValueError:
            print('Вводите параметры зарядов в формате [x y q]. '
                  'Координаты измеряются в сантиметрах, заряд - в кулонах, '
                  'поддерживается научная нотация через e.')

    X, Y, Ex, Ey, V = calculate(charges)
    draw_graph(X, Y, Ex, Ey, V, charges)

if __name__ == '__main__':
    main()