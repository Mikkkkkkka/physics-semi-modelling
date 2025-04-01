import numpy as np
import matplotlib.pyplot as plt

# const
k = 8.988e9

x_min, x_max = -5, 5
y_min, y_max = -5, 5


def calculate(charges):
    density = 500  # Плотность сетки
    x = np.linspace(x_min, x_max, density)
    y = np.linspace(y_min, y_max, density)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for charge in charges:
        x0, y0, q = charge
        dx = X - x0
        dy = Y - y0
        r_squared = dx ** 2 + dy ** 2
        mask = r_squared < 1e-12
        r_squared[mask] = 1e-12
        E = k * q / r_squared
        Ex += E * dx / np.sqrt(r_squared)
        Ey += E * dy / np.sqrt(r_squared)

    return X, Y, Ex, Ey


def draw_graph(X, Y, Ex, Ey, charges):
    plt.figure(figsize=(8, 6))
    color = np.log(np.sqrt(Ex ** 2 + Ey ** 2))  # Цвет по модулю поля
    plt.streamplot(X, Y, Ex, Ey, color=color, cmap='inferno', linewidth=1, density=2)

    # Отображение зарядов
    for charge in charges:
        x0, y0, q = charge
        if q > 0:
            plt.plot(x0, y0, 'ro', markersize=10)
        else:
            plt.plot(x0, y0, 'bo', markersize=10)

    plt.title('Электростатическое поле системы точечных зарядов')
    plt.xlabel('X')
    plt.ylabel('Y')
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

    X, Y, Ex, Ey = calculate(charges)
    draw_graph(X, Y, Ex, Ey, charges)


if __name__ == '__main__':
    main()
