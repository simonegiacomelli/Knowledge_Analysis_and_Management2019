import sys

import javalang
import os
import pandas as pd
from shutil import copyfile



def getFields(javaClass):
    return [dec.name for field in javaClass.fields for dec in field.declarators]


def getMethods(javaClass):
    return set([method for method in javaClass.methods])


def loop_node(method, referenceType):
    result = set()

    for path, node in method:
        if type(node) is referenceType and type(node) is not javalang.tree.ClassDeclaration:
            result.add(node)

    return list(result)


def getFieldsAccessedByMethod(method):
    return loop_node(method, javalang.tree.MemberReference)


def getMethodsAccessedByMethod(method):
    return loop_node(method, javalang.tree.MethodInvocation)


def getClass(source_path):
    with open(source_path, "r") as file_handle:
        source = file_handle.read()

    tree = javalang.parse.parse(source)

    source_no_extension = os.path.splitext(os.path.basename(source_path))[0]

    for tree_path, node in tree:
        if type(node) is javalang.tree.ClassDeclaration and node.name == source_no_extension:
            return node

    return None


def extract_feature_vectors(java_sorce, feature_vector):
    javaClass = getClass(java_sorce.path)
    # print("Processing class:", javaClass.name)
    fields = set(getFields(javaClass))
    # print("Fields:", len(fields))
    methods = getMethods(javaClass)
    methods_name = list(set([m.name for m in methods]))
    # print("Methods:", len(methods))
    df = pd.DataFrame(columns=fields)
    df.index.name = 'method_name'
    for method in methods:

        # create row if the method is not yet contemplated
        if method.name not in df.index:
            df.loc[method.name] = pd.Series()

        for field in getFieldsAccessedByMethod(method):
            if field.member in fields:
                df.loc[method.name, field.member] = 1

        for methodInvocation in getMethodsAccessedByMethod(method):
            if methodInvocation.member in methods_name:
                df.loc[method.name, methodInvocation.member] = 1

    df = df.fillna(0)
    for col in df:
        df[col] = df[col].astype('int')

    # remove columns with all zeroes
    df = df.loc[:, (df != 0).any(axis=0)]
    print(javaClass.name, df.shape)

    feature_vector.pd_to_csv(df)


def header():
    print('Class_name (#feature vectors, #attributes)')


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'auto':
        # extract_feature_vectors('./myjavasrc/B.java')
        # extract_feature_vectors('./myjavasrc/A.java')
        # src = './xerces2-javalang/xerces2-j-trunk/src'
        header()
        for gf in common.god_files:
            extract_feature_vectors(gf.java_source, gf.feature_vector)
    else:
        if len(sys.argv) != 3:
            print('wrong number of parameters')
            exit(1)
        java_source = sys.argv[1]
        feature_vector = common.File(sys.argv[2])

        if not common.File(feature_vector).check(must_exist=[java_source], must_not_exist=[feature_vector]):
            return

        header()

        extract_feature_vectors(java_source, feature_vector)


if __name__ == '__main__':
    main()
