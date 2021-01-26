#!/bin/env python
import sys
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
row_names = []
for matrix_fn, names_fn in zip(matrix_fofh,names_fofh):
    names = name_matching(names_fn.rstrip())
    m = pd.read_csv(matrix_fn.rstrip(),sep="\t",index_col=0)
    new_names = change_names(names,list(m.index))
    row_names += new_names
    m.index = new_names
    if index == 0:
        new_matrix = m
    else:
        new_matrix = new_matrix.merge(m,how='outer')
        #new_matrix = new_matrix.set_index('Subject').join(m.set_index('Subject'))
    index += 1

new_matrix.index = row_names
new_matrix.to_csv(merged_matrix,sep="\t",index_label='Subject')


