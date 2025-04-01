import numpy as np
import matplotlib.pyplot as plt

# Константы
G = 6.6743e-11

def calculate(m1, m2):
    x_space = np.linspace(-5, 5, 100)
    y_space = np.linspace(-5, 5, 100)

    x, y = np.meshgrid(x_space, y_space)

    r = np.sqrt(x ** 2 + y ** 2)
    u = (G * m1 * m2) / (r ** 2)
    u[r == 0] = 0

    return x, y, u


def draw_graph(x, y, u):
    plt.figure(figsize=(10, 6))

    plt.contourf(x, y, u, levels=50, cmap='viridis')
    plt.colorbar(label='Потенциальная энергия U(x, y)')

    plt.title('Распределение потенциальной энергии U(x, y)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()

    plt.show()


def main():
    m1 = float(input("Введите массу одного тела (кг): "))
    m2 = float(input("Введите массу второго тела (кг): "))

    x, y, u = calculate(m1, m2)

    draw_graph(x, y, u)


if __name__ == '__main__':
    main()