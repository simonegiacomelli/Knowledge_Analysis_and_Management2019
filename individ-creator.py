from owlready2 import *
import os
import sys
from glob import glob

import javalang
from owlready2 import *


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
        fqdn = package_name + '.' + class_node.name
        print(f'  processing {fqdn}')
        class_instance.name = fqdn
        class_instance.jname.append(class_node.name)
        for dec in class_node.body:
            type_name = type(dec).__name__
            if type_name == 'MethodDeclaration':
                dec_instance = onto[type_name]()
                dec_instance.jname.append(dec.name)
                class_instance.body.append(dec_instance)
            elif type_name == 'FieldDeclaration':
                pass
            elif type_name == 'ConstructorDeclaration':
                pass

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

    # TODO ##for each class member (MethodDeclaration/FieldDeclaration/ConstructorDeclaration) in the "body" of a
    #  ClassDeclaration, create a MethodDeclaration/FieldDeclaration/ ConstructorDeclaration instance and add (
    #  append) the member instance to the property "body" of the ClassDeclaration instance ## make sure that all
    #  individuals are declared to be different by calling AllDifferent (otherwise counting is not possible during
    #  bad smell detection)
    onto.save('tree2.owl')


if __name__ == '__main__':
    main()
