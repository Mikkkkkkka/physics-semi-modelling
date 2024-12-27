# const
EPS0 = 8.8541878128e-12  # Ф/м

dielectrics = [
    1.0,        # Вакуум
    1.00059,    # Воздух
    5.0,        # Стекло
    80.0        # Вода
]


def calculate_stays_connected(U, C, d):
    Q_end = C * U
    E_end = U / d
    return Q_end, E_end


def calculate_disconnects(Q0, C, d):
    Q_end = Q0
    U_end = Q_end / C
    E_end = U_end / d
    return Q_end, U_end, E_end


def main():
    print("Расчёт параметров плоского конденсатора.\n")
    while True:
        try:
            U = float(input("Введите напряжение (U) (В): "))
            d = float(input("Введите расстояние между пластинами (d) (м): "))
            S = float(input("Введите площадь пластин (S) (м^2): "))
            print('Поддерживаемые диэлектрики:')
            print('1. Вакуум')
            print('2. Воздух')
            print('3. Стекло')
            print('4. Вода')
            dielectric_input = int(input("Введите номер диэлектрика: "))
            connected_input = input("Остаётся ли конденсатор подключённым? (y / n) [y]: ").strip().lower()
            break

        except ValueError:
            print("Ошибка: Пожалуйста вводите числовые значения")

    epsilon_r = dielectrics[dielectric_input]
    C = EPS0 * epsilon_r * S / d
    Q0 = C / epsilon_r * U

    if connected_input == 'n':
        Q_end, U_end, E_end = calculate_disconnects(Q0, C, d)
        print("\nРезультаты (конденсатор был отключён):")
        print(f"- Ёмкость (C)       = {C:.4e} Ф")
        print(f"- Заряд (Q)         = {Q_end:.4e} Кл (не изменился)")
        print(f"- Новое (U)         = {U_end:.4e} В")
        print(f"- Напряжённость (E) = {E_end:.4e} В/м")
    else:
        Q_end, E_end = calculate_stays_connected(U, C, d)
        print("\nРезультаты: (конденсатор остался подключённым):")
        print(f"- Ёмкость (C)       = {C:.4e} Ф")
        print(f"- Заряд (Q)         = {Q_end:.4e} Кл")
        print(f"- Напряжённость (E) = {E_end:.4e} В/м")


if __name__ == "__main__":
    main()
