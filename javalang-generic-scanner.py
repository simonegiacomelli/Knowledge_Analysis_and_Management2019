import os
from glob import glob

import javalang
import pandas as pd
import sys

source_folder_path = "./android-chess"
if len(sys.argv) > 1:
    source_folder_path = sys.argv[1]

if not os.path.isdir(source_folder_path):
    print('Folder ', source_folder_path, 'not found')
    exit(0)


source_files_path = [y for x in os.walk(source_folder_path) for y in glob(os.path.join(x[0], '*.java'))]

df = pd.DataFrame(columns=list(['method_count', 'source_path']))
df.index.names = ['class_name']
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
            df.loc[node.name] = [len(node.methods), source_path.replace(source_folder_path, "")]

df.to_csv('all_parsed_source.csv')
method_count_col = df["method_count"]
print("Dataframe rows:", len(df.index))
print("method_count statistics:")
print("mean", method_count_col.mean())
print("max", method_count_col.max())
print("std", method_count_col.std())

boundary = method_count_col.mean() + 6 * method_count_col.std()

print("lower limit to be a god class:", boundary)

god_classes = df[df['method_count'] > boundary]
print("God classes:")
pd.set_option('max_colwidth', 800)
print(god_classes)
