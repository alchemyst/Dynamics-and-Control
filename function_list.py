#!/usr/bin/env python3
import ast
import sys
import nbformat
import collections
from link import link

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
all_functions = set()

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
                # print(f"Parse failed in {f} on this block:")
                # print(block)
                continue

            finder.visit(parsed)
            for func in finder.functions:
                function_index[func].add(f)
            all_functions.update(finder.functions)

known_prefixes = ['numpy', 'scipy',
                  'sympy', 'mpmath', 'pandas',
                  'plt',
                  'control',
                  # 'tclab',
                  ]

sortedfunctions = list(all_functions)
sortedfunctions.sort()

def announce(func):
    links = ", ".join([link(f) for f in function_index[func]])
    print(f'* `{func}`: {links}')

for prefix in known_prefixes:
    print(f"# {prefix}")
    print()
    for func in sortedfunctions:
        if func.startswith(prefix + '.'):
            announce(func)
            all_functions.remove(func)
    print()

print('# Other')
for func in sorted(all_functions):
    announce(func)
