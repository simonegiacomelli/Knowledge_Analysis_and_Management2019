import ast
from pprint import pprint
from owlready2 import *
import types


def main():
    with open("tree.py", "r") as source:
        tree = ast.parse(source.read())

    onto = get_ontology("http://usi.ch/proj1.owl")

    analyzer = Analyzer(onto)
    analyzer.visit(tree)

    onto.save('onto.owl')


class Analyzer(ast.NodeVisitor):
    def __init__(self, onto):
        self.onto = onto

    def visit_ClassDef(self, node: ast.ClassDef):
        x: ast.Name
        print(f'visit_ClassDef {node.name} {[x.id for x in node.bases]}')
        bases = tuple([self.decodeBase(b) for b in node.bases])
        with self.onto:
            types.new_class(node.name, bases)

    def decodeBase(self, base):
        return Thing if base.id == 'Node' else self.onto[base.id]


if __name__ == "__main__":
    main()
