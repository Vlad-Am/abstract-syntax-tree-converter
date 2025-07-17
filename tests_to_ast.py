import json
import sys

from sympy.parsing.sympy_parser import parse_expr

DEFAULT_INPUT_FILE = 'tests.json'
DEFAULT_OUTPUT_FILE = 'tests_ast.json'
TOL = 1e-4

# --- Функция для преобразования sympy-выражения в AST ---
def sympy_to_ast(expr):
    if expr.is_Number:
        return {"type": "const", "value": float(expr)}
    if expr.is_Symbol:
        return {"type": "var", "name": str(expr)}
    if expr.is_Add:
        args = list(expr.args)
        node = sympy_to_ast(args[0])
        for arg in args[1:]:
            node = {"type": "add", "left": node, "right": sympy_to_ast(arg)}
        return node
    if expr.is_Mul:
        args = list(expr.args)
        node = sympy_to_ast(args[0])
        for arg in args[1:]:
            node = {"type": "mul", "left": node, "right": sympy_to_ast(arg)}
        return node
    if expr.is_Pow:
        base, exp = expr.args
        return {"type": "pow", "left": sympy_to_ast(base), "right": sympy_to_ast(exp)}
    if expr.func.__name__ == 'sqrt':
        return {"type": "func", "name": "sqrt", "args": [sympy_to_ast(expr.args[0])]}
    if expr.func.__name__ == 'log':
        if len(expr.args) == 2:
            return {"type": "func", "name": "log", "args": [sympy_to_ast(expr.args[0]), sympy_to_ast(expr.args[1])]}
        else:
            return {"type": "func", "name": "ln", "args": [sympy_to_ast(expr.args[0])]}
    if expr.func.__name__ == 'floor':
        return {"type": "func", "name": "floor", "args": [sympy_to_ast(expr.args[0])]}
    if expr.func.__name__ == 'ceiling':
        return {"type": "func", "name": "ceil", "args": [sympy_to_ast(expr.args[0])]}
    if expr.func.__name__ == 'round':
        return {"type": "func", "name": "round", "args": [sympy_to_ast(expr.args[0])]}
    if expr.func.__name__ == 'NegativeOne':
        return {"type": "const", "value": -1}
    if expr.func.__name__ == 'sub':
        left, right = expr.args
        return {"type": "sub", "left": sympy_to_ast(left), "right": sympy_to_ast(right)}
    if expr.is_Add and any(a.is_Number and a < 0 for a in expr.args):
        pass
    if expr.is_Add:
        args = list(expr.args)
        node = sympy_to_ast(args[0])
        for arg in args[1:]:
            if arg.is_Number and arg < 0:
                node = {"type": "sub", "left": node, "right": sympy_to_ast(-arg)}
            else:
                node = {"type": "add", "left": node, "right": sympy_to_ast(arg)}
        return node
    raise NotImplementedError(f"Неизвестный тип: {expr}")

# --- Основная логика ---
def main():
    # Аргументы: [input_file] [output_file]
    input_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_FILE
    output_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_FILE
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            tests = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения {input_file}: {e}")
        sys.exit(1)

    output = []
    all_ok = True
    for idx, test in enumerate(tests, 1):
        formula_str = test.get('formula')
        testcases = test.get('testcases', [])
        print(f"Проверка формулы {idx}: {formula_str}")
        formula_ok = True
        # Парсим формулу
        try:
            expr = parse_expr(formula_str, evaluate=False)
        except Exception as e:
            print(f"  [ERROR] Формула не парсится: {e}")
            all_ok = False
            formula_ok = False
            continue
        # Генерируем AST
        try:
            ast = sympy_to_ast(expr)
        except Exception as e:
            print(f"  [ERROR] Не удалось построить AST: {e}")
            all_ok = False
            formula_ok = False
            continue
        # Проверяем тесткейсы
        for t_idx, case in enumerate(testcases, 1):
            variables = case.get('variables', {})
            expected = case.get('expected_result')
            try:
                result = float(expr.evalf(subs=variables))
            except Exception as e:
                print(f"  [ERROR] Тест {t_idx}: ошибка вычисления: {e}")
                all_ok = False
                formula_ok = False
                continue
            if abs(result - expected) > TOL:
                print(f"  [ERROR] Тест {t_idx}: вычислено {result}, ожидается {expected}, разница {abs(result-expected)}")
                all_ok = False
                formula_ok = False
        if formula_ok:
            print("  OK")
        # Добавляем в выходной массив
        output.append({
            "formula_ast": ast,
            "testcases": testcases
        })
    if not all_ok:
        print(f"\nОбнаружены ошибки. Файл {output_file} не будет создан.")
        sys.exit(1)
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nГотово! Сохранён файл {output_file}")
    print("Все формулы и тесты корректны.")

if __name__ == '__main__':
    main()
