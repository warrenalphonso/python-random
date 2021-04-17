"""
Use the ast module to get sets of:
- variable names
- function names
- libraries imported
from a file.

Inspired by: https://stackoverflow.com/a/51118277/13697995

TODO:
- Test parse_file:
    - try, except, else, finally
    - if, elif, else
    - for, for with tuple (for i, j in zip(...))
    - Import and import from and import as
    - Functions, and lambdas (lambdas go in variable names), and classes, and
      methods
"""
import ast

variables: set[str] = set()
functions: set[str] = set()
imports: set[str] = set()


def get_variables(node) -> set:
    """Get variables on NODE, doesn't recurse."""
    if isinstance(node, ast.Assign):
        return set(name.id for name in node.targets
                   if isinstance(name, ast.Name))
    # Get variable name in for loop (just the target, not iterable)
    elif isinstance(node, ast.For):
        if isinstance(node.target, ast.Name):
            return set((node.target.id,))
        elif isinstance(node.target, (ast.Tuple, ast.List)):
            return set(el.id for el in node.target.elts
                       if isinstance(el, ast.Name))
    return set()


def get_functions(node) -> set:
    if isinstance(node, ast.FunctionDef):
        return set((node.name,))
    # TODO: Get argument names?
    if isinstance(node, ast.ClassDef):
        return set((node.name,))
    return set()


def get_imports(node) -> set:
    if isinstance(node, ast.Import):
        return set(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom):
        return set((node.module,))
    return set()


def extract_names(node):
    global variables, functions, imports
    variables |= get_variables(node)
    functions |= get_functions(node)
    imports |= get_imports(node)


def parse_node(node) -> None:
    if hasattr(node, "body"):
        for subnode in node.body:
            extract_names(subnode)
            parse_node(subnode)
    # For try blocks
    if hasattr(node, "handlers"):
        for subnode in node.handlers:
            extract_names(subnode)
            parse_node(subnode)
    if hasattr(node, "orelse"):
        for subnode in node.orelse:
            extract_names(subnode)
            parse_node(subnode)
    if hasattr(node, "finalbody"):
        for subnode in node.finalbody:
            extract_names(subnode)
            parse_node(subnode)


def parse_file(filename: str) -> tuple[set]:
    try:
        parsed_ast = ast.parse(open(filename).read())
    except Exception as e:
        # TODO: Getting an error in Django...
        return set(), set(), set(), ""
    else:
        parse_node(parsed_ast)
        return variables, functions, imports, filename
