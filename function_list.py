#!/usr/bin/env python3
import ast
import sys
import nbformat
import collections

def validline(line):
    return not (line.startswith('%')
                or line.endswith('?')
                or line.endswith('.')
                or line.startswith('!'))


def namer(obj):
    if isinstance(obj, ast.Name):
        return obj.id
    elif isinstance(obj, ast.Attribute):
        return namer(obj.value) + '.' + obj.attr
    else:
        raise(ValueError)


class FunctionFinder(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.functions = set()
    def visit_Call(self, node):
        try:
            self.functions.add(namer(node.func))
        except ValueError:
            pass

function_index = collections.defaultdict(set)

for f in sys.argv[1:]:
    finder = FunctionFinder()
    nb = nbformat.read(f, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            block = '\n'.join([line for line in cell.source.split('\n')
                               if validline(line)])
            # print(block)
            try:
                parsed = ast.parse(block)
            except:
                print(f"Parse failed in {f} on this block:")
                print(block)
                continue

            finder.visit(parsed)
            function_index[f].update(finder.functions)
