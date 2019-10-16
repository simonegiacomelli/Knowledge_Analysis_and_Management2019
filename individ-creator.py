from glob import glob

import javalang
from owlready2 import *


# TODO
## make sure that all
#  individuals are declared to be different by calling AllDifferent (otherwise counting is not possible during
#  bad smell detection)

# TODO refactoring in OOP?
def params_to_str(method_declaration):
    res = ','.join([p.type.name for p in method_declaration.parameters])
    if len(method_declaration.parameters) > 0:
        print(res)
    return res


def main():
    onto = get_ontology("file://tree.owl")
    onto.load()

    source_folder_path = "./android-chess/app/src/main/java"
    if len(sys.argv) > 1:
        source_folder_path = sys.argv[1]

    if not os.path.isdir(source_folder_path):
        print('Folder ', source_folder_path, 'not found')
        exit(0)

    source_files_path = [y for x in os.walk(source_folder_path) for y in glob(os.path.join(x[0], '*.java'))]
    filter_types = {'ClassDeclaration', 'MethodDeclaration', 'FieldDeclaration', 'ConstructorDeclaration'}

    def process_class(class_node, package_name):
        class_instance = onto["ClassDeclaration"]()
        class_fqn = package_name + '.' + class_node.name
        print(f'  processing {class_fqn}')
        class_instance.name = class_fqn
        class_instance.jname.append(class_node.name)
        for dec in class_node.body:
            type_name = type(dec).__name__
            if type_name == 'MethodDeclaration':
                dec_instance = onto[type_name]()
                class_instance.body.append(dec_instance)
                method_fqn = class_fqn + '.' + dec.name + f'({params_to_str(dec)})'
                print(f'     method {method_fqn}')
                dec_instance.jname.append(dec.name)
                dec_instance.name = method_fqn
            elif type_name == 'FieldDeclaration':
                for f in dec.declarators:
                    field_fqn = class_fqn + '.' + f.name + '[field]'
                    print(f'     field {field_fqn}')
                    dec_instance = onto[type_name]()
                    class_instance.body.append(dec_instance)
                    dec_instance.jname.append(f.name)
                    dec_instance.name = field_fqn
            elif type_name == 'ConstructorDeclaration':
                constructor_fqn = class_fqn + '.$constructor$.' + dec.name + f'({params_to_str(dec)})'
                print(f'     constructor {constructor_fqn}')
                dec_instance = onto[type_name]()
                class_instance.body.append(dec_instance)
                dec_instance.jname.append(dec.name)
                dec_instance.name = constructor_fqn

    def process_types(types, package_name):
        for node in types:
            if type(node) is javalang.tree.ClassDeclaration:
                process_class(node, package_name)
                process_types(node.body, package_name + '.' + node.name)

    for source_path in source_files_path:
        with open(source_path, "r") as file_handle:
            source = file_handle.read()
        print('parsing', source_path)
        tree = javalang.parse.parse(source)

        process_types(tree.types, tree.package.name)

    onto.save('tree2.owl')


if __name__ == '__main__':
    main()
