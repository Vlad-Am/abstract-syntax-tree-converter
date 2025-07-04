using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


class FormulaAstEvalTests
{
    static void Main(string[] args)
    {
        string inputFile = args.Length > 0 ? args[0] : "tests_ast.json";
        if (!File.Exists(inputFile))
        {
            Console.WriteLine($"Файл {inputFile} не найден.");
            return;
        }
        var testsAstJson = File.ReadAllText(inputFile);
        var tests = JArray.Parse(testsAstJson);

        int total = 0;
        int passed = 0;
        int formulaIdx = 1;
        foreach (var test in tests)
        {
            var formulaAst = test["formula_ast"];
            var testcases = test["testcases"] as JArray;
            Console.WriteLine($"Формула {formulaIdx}:");
            int localTotal = 0, localPassed = 0;
            int idx = 1;
            foreach (var testcase in testcases)
            {
                var variables = testcase["variables"].ToObject<Dictionary<string, float>>();
                float expected = testcase["expected_result"].ToObject<float>();
                float result = FormulaAstEval.EvalAst(formulaAst, variables);
                bool ok = Math.Abs(result - expected) < 1e-4f;
                if (ok)
                {
                    localPassed++;
                    // Не выводим ничего если тест пройден
                }
                else
                {
                    Console.WriteLine($"  Тест {idx}: вычислено={result}, ожидается={expected}, совпадает={ok}");
                }
                idx++;
            }
            Console.WriteLine($"  Пройдено {localPassed} из {testcases.Count} тестов.\n");
            total += testcases.Count;
            passed += localPassed;
            formulaIdx++;
        }
        Console.WriteLine($"Итого: пройдено {passed} из {total} тестов. {(passed == total ? "ВСЕ ОК" : "Есть ошибки!")}");
    }
}