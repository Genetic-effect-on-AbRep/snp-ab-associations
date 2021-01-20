#!/bin/env python
import sys
import pandas as pd
import copy 

gene_matrix_infn = sys.argv[1]
snp_matrix_infn = sys.argv[2]
outdir = sys.argv[3]
namesfn = sys.argv[4]

gene_matrix_outfn = "%s/gene.txt" % outdir
snp_matrix_outfn = "%s/snp.txt" % outdir

def namekeys(namesfn):
    gene_keys = {}
    snp_keys = {}
    with open(namesfn,'r') as fh:
        for line in fh:
            line = line.rstrip().split('\t')
            name = line[0]
            gene = line[1]
            snp = line[2]            
            gene_keys[gene] = name
            snp_keys[snp] = name
    return (gene_keys,snp_keys)

def check_samples(columns,keys,matrix):
    samples = []
    for column in columns:
        if column in keys:
            samples.append(column)
        else:
            x=1
            #print("%s in %s matrix not found in name key" % (column,matrix))
    return samples
    
def gene_matrix_samples(matrixfn,keys):
    matrix = pd.read_csv(matrixfn,sep="\t",index_col=False,header=None)
    columns = list(matrix.iloc[:, 0])[1:]
    samples = check_samples(columns,keys,"gene")
    return samples

def snp_matrix_samples(matrixfn,keys):
    matrix = pd.read_csv(matrixfn,sep="\t",nrows=1)
    columns = list(matrix)
    samples = check_samples(columns,keys,"snp")
    return samples

def get_selected_samples(columns,keys):
    selected_samples = []
    new_header = []
    for column in columns:        
        if column not in keys:
            continue
        if keys[column] not in samples:
            continue
        selected_samples.append(column)
        new_header.append(keys[column])
    return (selected_samples,new_header)

def gene_matrix_transform(matrixfn,keys,samples):
    matrix = pd.read_csv(matrixfn,sep="\t",header=0,index_col=0)
    matrix = matrix.T
    columns = map(str,list(matrix))
    matrix.columns = map(str,list(matrix))
    selected_samples,new_header = get_selected_samples(columns,keys)
    matrix = matrix[selected_samples]
    return (new_header,matrix)
    
def samples_in_common(gene_samples,snp_samples,gene_keys,snp_keys):
    gene = set()
    snp = set()
    for g in gene_samples:
        gene.add(gene_keys[g])
    for s in snp_samples:
        snp.add(snp_keys[s])
    common = list(gene & snp)
    print("Samples in common: %s" % "\t".join(common))
    return common

def snp_matrix_transform(matrixfn,keys,samples):
    matrix = pd.read_csv(matrixfn,sep="\t",header=0,index_col=0)
    columns = map(str,list(matrix))
    selected_samples,new_header = get_selected_samples(columns,keys)
    matrix = matrix[selected_samples]
    return (new_header,matrix)

gene_keys,snp_keys = namekeys(namesfn)
gene_samples = gene_matrix_samples(gene_matrix_infn,gene_keys)
snp_samples = snp_matrix_samples(snp_matrix_infn,snp_keys)
samples = samples_in_common(gene_samples,snp_samples,gene_keys,snp_keys)

gene_header,gene_matrix = gene_matrix_transform(gene_matrix_infn,gene_keys,samples)
gene_matrix.to_csv(gene_matrix_outfn,sep="\t",index_label="id",header=gene_header)

snp_header,snp_matrix = snp_matrix_transform(snp_matrix_infn,snp_keys,samples)
snp_matrix.to_csv(snp_matrix_outfn,sep="\t",index_label="id",header=snp_header)

