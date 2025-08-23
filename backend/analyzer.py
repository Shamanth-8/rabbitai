import ast
import radon.complexity as radon_cc
from radon.metrics import mi_visit

def analyze_code(code: str):
    results = {}
    blocks = radon_cc.cc_visit(code)
    results["complexity"] = [f"{b.name}: {b.complexity}" for b in blocks]
    results["maintainability_index"] = mi_visit(code, True)

    tree = ast.parse(code)
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    results["functions"] = functions
    results["function_count"] = len(functions)
    return results