import sympy


def V_node(node_idx, V):
    if node_idx == 0:
        return 0
    else:
        return V[node_idx - 1]


def calculate(n, branches, V):

    current_balance = {node: 0 for node in range(1, n)}  # узел 0 не пишем
    equations = []
    source_equations = []

    for (start_node, end_node, elem_type, val) in branches:
        v_s = V_node(start_node, V)
        v_e = V_node(end_node, V)

        if elem_type == 'R':
            I = (v_s - v_e) / val

            if start_node != 0:
                current_balance[start_node] += I
            if end_node != 0:
                current_balance[end_node] -= I

        elif elem_type == 'E':
            source_equations.append(v_s - v_e - val)


            I_symbol = sympy.Symbol(f'I_E_{start_node}_{end_node}', real=True)

            if start_node != 0:
                current_balance[start_node] += I_symbol
            if end_node != 0:
                current_balance[end_node] -= I_symbol

    for node in range(1, n):
        eq = current_balance[node]
        equations.append(eq)

    equations.extend(source_equations)

    all_symbols = set()
    for eq in equations:
        all_symbols.update(eq.free_symbols)

    all_symbols = list(all_symbols)

    return sympy.solve(equations, all_symbols, dict=True)


def main():

    print('Потенциал узла 0 - 0 В')
    n = int(input("Введите количество узлов (включая узел 0): "))
    m = int(input("Введите количество ветвей: "))

    edges = []

    print("\nВведите параметры каждого ребра")
    print("(начальный узел, конечный узел, тип узла и сопротивление или ЭДС узла в зависимости от типа):")
    print('Поддерживаемые типы узлов: R - резистор, E - ЭДС')
    print("Например: 0 1 E 5\n")

    for i in range(m):
        line = input(f"Ребро {i + 1}: ").strip().split()
        start_node = int(line[0])
        end_node = int(line[1])
        elem_type = line[2].upper()
        value = float(line[3])
        edges.append((start_node, end_node, elem_type, value))

    V = sympy.symbols(f'V1:{n}', real=True)

    solutions = calculate(n, edges, V)

    if not solutions:
        print("\nСистема не имеет решения или переопределена. Проверьте входные данные.")
        return

    sol = solutions[0]

    print("\nРезультаты:")
    print("Узловые потенциалы (В):")
    for node_idx in range(1, n):
        v_sym = V[node_idx - 1]  # это символ V1..V_{n-1}
        value_sol = sol.get(v_sym, 0)
        print(f"  V({node_idx}) = {value_sol} В")

    print("\nТок в ветвях (А):")

    for idx, (start_node, end_node, elem_type, val) in enumerate(edges, 1):
        start = V_node(start_node, V)
        end = V_node(end_node, V)

        if elem_type == 'R':
            I_expr = (start - end) / val
            I_val = I_expr.subs(sol)
            print(f"  Ребро {idx} (из {start_node} в {end_node}): R={val} Ом, I = {I_val.evalf()} А")
        else:
            I_symbol = sympy.Symbol(f'I_E_{start_node}_{end_node}', real=True)
            I_val = sol.get(I_symbol, 0)
            print(f"  Ребро {idx} (из {start_node} в {end_node}): E={val} В,  I = {I_val.evalf()} А")


if __name__ == "__main__":
    main()