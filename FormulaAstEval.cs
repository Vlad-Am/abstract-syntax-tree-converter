using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


public class FormulaAstEval
{
    public static float EvalAst(JToken node, Dictionary<string, float> vars)
    {
        string type = node["type"].ToString();
        switch (type)
        {
            case "const":
                return node["value"].ToObject<float>();
            case "var":
                return vars[node["name"].ToString()];
            case "add":
                return EvalAst(node["left"], vars) + EvalAst(node["right"], vars);
            case "sub":
                return EvalAst(node["left"], vars) - EvalAst(node["right"], vars);
            case "mul":
                return EvalAst(node["left"], vars) * EvalAst(node["right"], vars);
            case "pow":
                return (float)Math.Pow(EvalAst(node["left"], vars), EvalAst(node["right"], vars));
            case "func":
                string fname = node["name"].ToString();
                var args = node["args"] as JArray;
                if (fname == "sqrt")
                    return (float)Math.Sqrt(EvalAst(args[0], vars));
                if (fname == "log")
                    return (float)Math.Log(EvalAst(args[0], vars), EvalAst(args[1], vars));
                if (fname == "ln")
                    return (float)Math.Log(EvalAst(args[0], vars));
                if (fname == "round")
                    return (float)MathF.Round(EvalAst(args[0], vars));
                if (fname == "floor")
                    return (float)MathF.Floor(EvalAst(args[0], vars));
                if (fname == "ceil")
                    return (float)MathF.Ceiling(EvalAst(args[0], vars));
                throw new NotImplementedException($"Функция {fname} не поддерживается");
            default:
                throw new NotImplementedException($"Тип {type} не поддерживается");
        }
    }
}