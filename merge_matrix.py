#!/bin/env python
import sys
import numpy as np
import pandas as pd

matrix_fofn = sys.argv[1]
names_fofn = sys.argv[2]
merged_matrix = sys.argv[3]

matrix_fofh = open(matrix_fofn,'r')
names_fofh = open(names_fofn,'r')

def name_matching(fn):
    names = {}
    with open(fn,'r') as fh:
        for line in fh:
            line = line.rstrip().split('\t')
            names[line[0]] = line[1]
    return names

def change_names(map_,current_names):
    names = []
    for n in current_names:
        names.append(map_[str(n)])
    return names

index = 0    
new_matrix = None
for matrix_fn, names_fn in zip(matrix_fofh,names_fofh):
    names = name_matching(names_fn.rstrip())
    m = pd.read_csv(matrix_fn.rstrip(),sep="\t",index_col=0)
    new_names = change_names(names,list(m.index))
    m.index = new_names
    m['samples'] = new_names
    if index == 0:
        new_matrix = m
    else:
        common_columns = list(np.intersect1d(new_matrix.columns,m.columns))
        new_matrix = new_matrix.merge(m,how='outer',on=common_columns)
    index += 1

new_matrix.index = new_matrix['samples']
new_matrix.drop(['samples'],axis=1,inplace=True)
new_matrix.to_csv(merged_matrix,sep="\t",index_label='Subject',na_rep="NA")
