import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы
e = 1.6021766208e-19
m = 9.10938356e-31

# Дано
r = 0.075
R = 0.16
v_0 = 2e6
l = 0.24

y_0 = (r + R) / 2
v_y0 = 0.0

t = l / v_0
log_ratio = np.log(R / r)


def ode_system(t, Y, V0):
    y, vy = Y
    ay = (e * V0) / (m * log_ratio * y)
    return [vy, ay]


def solve_trajectory(V0):
    sol = solve_ivp(ode_system,
                    [0, t],
                    [y_0, v_y0],
                    args=(V0,),
                    dense_output=True,
                    rtol=1e-8,
                    atol=1e-10)
    return sol


def calculate():
    V0_min, V0_max = 0.1, 10.0
    for _ in range(50):
        V0_mid = 0.5 * (V0_min + V0_max)
        sol = solve_trajectory(V0_mid)
        y_end = sol.y[0, -1]
        if y_end > R:
            V0_max = V0_mid
        else:
            V0_min = V0_mid

    V0_opt = 0.5 * (V0_min + V0_max)
    sol_final = solve_trajectory(V0_opt)

    t_vals = np.linspace(0, t, 1000)
    y_vals = sol_final.sol(t_vals)[0]
    vy_vals = sol_final.sol(t_vals)[1]

    ay_vals = (e * V0_opt) / (m * log_ratio * y_vals)
    x_vals = v_0 * t_vals
    final_v = np.sqrt(v_0 ** 2 + vy_vals[-1] ** 2)

    return V0_opt, final_v, x_vals, y_vals, t_vals, vy_vals, ay_vals


def draw_graphs(x_vals, y_vals, t_vals, vy_vals, ay_vals):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(x_vals, y_vals, label='y(x)')
    plt.axhline(r, color='r', linestyle='--', label='r')
    plt.axhline(R, color='g', linestyle='--', label='R')
    plt.xlabel('x, м')
    plt.ylabel('y, м')
    plt.title('Траектория [y(x)]')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(t_vals, vy_vals)
    plt.xlabel('t, с')
    plt.ylabel('v_y, м/с')
    plt.title('Скорость по радиусу [v_y(t)]')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(t_vals, ay_vals)
    plt.xlabel('t, с')
    plt.ylabel('a_y, м/с^2')
    plt.title('Зависимость ускорения по y от времени [a_y(t)]')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(t_vals, y_vals)
    plt.xlabel('t, с')
    plt.ylabel('y, м')
    plt.title('Координата по y от времени [y(t)]')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    V0_opt, final_v, x_vals, y_vals, t_vals, vy_vals, ay_vals = calculate()

    print(f"Разность потенциалов V0: {V0_opt:.4f} В")
    print(f"Конечное положение y: {y_vals[-1]:.6f} м (должно быть ~{R} м)")
    print(f"Конечная полная скорость электрона: {final_v:.2e} м/с")
    print(f"Время пролета: {t:.2e} с")

    draw_graphs(x_vals, y_vals, t_vals, vy_vals, ay_vals)


if __name__ == '__main__':
    main()
