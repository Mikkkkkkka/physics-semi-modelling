import numpy as np
import matplotlib.pyplot as plt

# Начальные условия
h0 = 1.0
v0 = 0.0

# Временные параметры
def calculate(m, k, c):
    t_max = 10.0
    delta_t = 0.01

    # Инициализация массивов
    t = np.arange(0, t_max, delta_t)
    h_t = np.zeros_like(t)
    v_t = np.zeros_like(t)
    kyn_e_t = np.zeros_like(t)
    pot_e_t = np.zeros_like(t)
    full_e_t = np.zeros_like(t)

    # Установка начальных условий
    h_t[0] = h0
    v_t[0] = v0

    # Численное решение уравнений движения методом Эйлера
    for i in range(1, len(t)):
        # Расчет ускорения на текущем шаге
        a = (-k * h_t[i - 1] - c * v_t[i - 1]) / m

        # Обновление скорости и положения
        v_t[i] = v_t[i - 1] + a * delta_t
        h_t[i] = h_t[i - 1] + v_t[i - 1] * delta_t

        # Расчет энергий
        kyn_e_t[i] = 0.5 * m * v_t[i] ** 2
        pot_e_t[i] = 0.5 * k * h_t[i] ** 2
        full_e_t[i] = kyn_e_t[i] + pot_e_t[i]

    return t, kyn_e_t, pot_e_t, full_e_t

# Построение графиков энергий
def draw_graphs(t, ke, pe, e):
    plt.figure(figsize=(12, 6))

    plt.plot(t, ke, label='Кинетическая энергия')
    plt.plot(t, pe, label='Потенциальная энергия')
    plt.plot(t, e, label='Полная механическая энергия', linestyle='--')

    plt.title('Энергетические превращения при колебании груза на пружине')
    plt.xlabel('Время (с)')
    plt.ylabel('Энергия (Дж)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    m = float(input("Введите массу груза (кг): "))
    c = float(input("Введите коэффициент упругости: "))
    k = float(input("Введите коэффициент сопротивления среды: "))

    t, ke, pe, e = calculate(m, k, c)
    draw_graphs(t, ke, pe, e)


if __name__ == '__main__':
    main()