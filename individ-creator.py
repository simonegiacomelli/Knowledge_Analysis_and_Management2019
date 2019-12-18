import javalang
from owlready2 import *


def params_to_str(method_declaration):
    res = ','.join([p.type.name for p in method_declaration.parameters])
    return res


class PrettyPrint:
    def __init__(self):
        self.level = 0

    def print(self, *arg):
        print(' ' * (self.level * 3), end='')
        print(*arg)

    def inc(self):
        self.level += 1

    def dec(self):
        self.level -= 1


def main():
    onto = get_ontology("file://tree.owl")
    onto.load()

    source_folder_path = "./chess"
    if len(sys.argv) > 1:
        source_folder_path = sys.argv[1]

    if not os.path.isdir(source_folder_path):
        print('Folder ', source_folder_path, 'not found')
        exit(0)

    # source_files_path = [y for x in os.walk(source_folder_path) for y in glob(os.path.join(x[0], '*.java'))]
    source_files_path = [f for f in [os.path.join(source_folder_path, ent) for ent in os.listdir(source_folder_path)]
                         if os.path.isfile(f)]
    pp = PrettyPrint()

    def process_callable_declaration(callable, callable_instance):
        pp.inc()

        for dec in callable.parameters:
            type_name = type(dec).__name__
            dec_instance = onto[type_name]()
            callable_instance.parameters.append(dec_instance)

        if callable.body is None:
            pp.print('None!')
        else:
            def add_statements(stmts):
                if hasattr(stmts, 'statements'):
                    stmts = stmts.statements
                stats = [s for s in stmts if isinstance(s, javalang.tree.Statement)]
                for dec in stats:
                    type_name = type(dec).__name__
                    dec_instance = onto[type_name]()
                    callable_instance.body.append(dec_instance)
                    if hasattr(dec, 'body'):
                        add_statements(dec.body)

            add_statements(callable.body)

        pp.dec()

    def process_class(class_node, package_name):
        pp.inc()
        class_instance = onto["ClassDeclaration"]()
        class_fqn = package_name + '.' + class_node.name
        pp.print(f'processing {class_fqn}')
        class_instance.name = class_fqn
        class_instance.jname.append(class_node.name)
        pp.inc()
        for dec in class_node.body:
            type_name = type(dec).__name__
            if type_name == 'MethodDeclaration':
                dec_instance = onto[type_name]()
                class_instance.body.append(dec_instance)
                method_fqn = class_fqn + '.' + dec.name + f'({params_to_str(dec)})'
                pp.print(f'method {method_fqn}')
                dec_instance.jname.append(dec.name)
                dec_instance.name = method_fqn
                process_callable_declaration(dec, dec_instance)
            elif type_name == 'FieldDeclaration':
                for f in dec.declarators:
                    field_fqn = class_fqn + '.' + f.name + '[field]'
                    pp.print(f'field {field_fqn}')
                    dec_instance = onto[type_name]()
                    class_instance.body.append(dec_instance)
                    dec_instance.jname.append(f.name)
                    dec_instance.name = field_fqn
            elif type_name == 'ConstructorDeclaration':
                constructor_fqn = class_fqn + '.$constructor$.' + dec.name + f'({params_to_str(dec)})'
                pp.print(f'constructor {constructor_fqn}')
                dec_instance = onto[type_name]()
                class_instance.body.append(dec_instance)
                dec_instance.jname.append(dec.name)
                dec_instance.name = constructor_fqn
                process_callable_declaration(dec, dec_instance)
            else:
                pass
                # pp.print(f'else {type_name}')
                # process_types(dec, class_fqn)

        pp.dec()
        pp.dec()

    def process_types(types, package_name):
        for node in types:
            if type(node) is javalang.tree.ClassDeclaration:
                process_class(node, package_name)
                process_types(node.body, package_name + '.' + node.name)

    for source_path in source_files_path:
        with open(source_path, "r") as file_handle:
            source = file_handle.read()
        pp.print('parsing', source_path)
        tree = javalang.parse.parse(source)

        process_types(tree.types, tree.package.name)

    onto.save('tree2.owl')


if __name__ == '__main__':
    main()
