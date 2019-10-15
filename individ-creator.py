from owlready2 import *
import os
import sys
from glob import glob

import javalang
from owlready2 import *


def main():
    onto = get_ontology("file://tree.owl")
    onto.load()

    source_folder_path = "./android-chess/app/src/main"
    if len(sys.argv) > 1:
        source_folder_path = sys.argv[1]

    if not os.path.isdir(source_folder_path):
        print('Folder ', source_folder_path, 'not found')
        exit(0)

    source_files_path = [y for x in os.walk(source_folder_path) for y in glob(os.path.join(x[0], '*.java'))]

    for source_path in source_files_path:
        with open(source_path, "r") as file_handle:
            source = file_handle.read()
        print('parsing', source_path)
        tree = javalang.parse.parse(source)

        result = []
        for tree_path, node in tree:
            if type(node) is javalang.tree.ClassDeclaration:
                # and node.name+'.java' == os.path.basename(source_path):
                ## keeping the second condition yields to only 3 god classess. so I removed it
                # df.loc[node.name] = [len(node.methods), source_path.replace(source_folder_path, "")]
                cd = onto["ClassDeclaration"]()
                # cd.jname = node.name
                cd.jname.append(node.name)

    # TODO ##for each class member (MethodDeclaration/FieldDeclaration/ConstructorDeclaration) in the "body" of a
    #  ClassDeclaration, create a MethodDeclaration/FieldDeclaration/ ConstructorDeclaration instance and add (
    #  append) the member instance to the property "body" of the ClassDeclaration instance ## make sure that all
    #  individuals are declared to be different by calling AllDifferent (otherwise counting is not possible during
    #  bad smell detection)
    onto.save('tree2.owl')


if __name__ == '__main__':
    main()
