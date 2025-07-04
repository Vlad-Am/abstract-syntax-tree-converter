# LotW Formula Serialization

## Описание

Утилиты для сериализации и проверки математических формул между Python (сервер) и C# (клиент, например, Unity). Формулы и тесты описываются в json, преобразуются в AST, и могут быть проверены на обеих сторонах.

## Что такое AST?

**AST (Abstract Syntax Tree, абстрактное синтаксическое дерево)** — это структурированное представление формулы в виде вложенных объектов, где каждый узел — это операция, функция, переменная или константа.

**Пример формулы:**
```
2 * sqrt(x) + ln(y) - 5
```

**AST для этой формулы (схема):**
```
      (-)
     /   \
   (+)    5
  /   \
(*)    ln
/ \     |
2 sqrt  y
    |
    x
```

**AST в JSON:**
```json
{
  "type": "sub",
  "left": {
    "type": "add",
    "left": {
      "type": "mul",
      "left": { "type": "const", "value": 2 },
      "right": {
        "type": "func",
        "name": "sqrt",
        "args": [{ "type": "var", "name": "x" }]
      }
    },
    "right": {
      "type": "func",
      "name": "log2",
      "args": [{ "type": "var", "name": "y" }]
    }
  },
  "right": { "type": "const", "value": 5 }
}
```

---

## Структура
- `tests_to_ast.py` — Python-скрипт: читает файл с формулами и тестами, проверяет корректность, преобразует формулы в AST и сохраняет новый json.
- `FormulaAstEval.cs` — C#-утилита: читает AST и тесты, вычисляет значения, сверяет с эталоном.
- `tests_str.json` — пример входного файла с формулами-строками и тестами.
- `tests_ast.json` — выходной файл с формулами в виде AST.

## Использование

### 1. Проверка и преобразование формул (Python)

```sh
python tests_to_ast.py tests_str.json tests_ast.json
```
- На входе: `tests_str.json` (или свой файл)
- На выходе: `tests_ast.json` (или свой файл)
- Если есть ошибки в формулах или тестах — выходной файл не создаётся, ошибки выводятся в консоль.

### 2. Проверка вычислений (C#)

```sh
dotnet run --project . -- tests_ast.json
```
- На входе: `tests_ast.json` (или свой файл)
- Выводит только ошибки (если есть), а также статистику по тестам.

## Пример структуры входного файла

```json
[
  {
    "formula": "floor(10 * pow(level, 1.1) + 0.5)",
    "testcases": [
      { "variables": {"level": 1}, "expected_result": 10 },
      { "variables": {"level": 2}, "expected_result": 21 }
    ]
  }
]
```

## Поддерживаемые функции
- sqrt, log, ln, pow
- floor, ceil, 
- вместо round: floor(... + 0.5)

## Зависимости
- Python: `sympy`
- C#: `Newtonsoft.Json`
