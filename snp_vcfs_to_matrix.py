#!/bin/env python
import sys
import vcf
import pandas as pd

vcf_fofn = sys.argv[1]
matrixfn = sys.argv[2]

def transform_genotype(genotype):
    t = None
    function = {
        "0/0": 0,
        "0/1": 1,
        "1/2": 2
    }
    if genotype in function:
        t = function[genotype]
    return t
    
def vcf_genotypes(fn,chrom="igh"):
    vcf_reader = vcf.Reader(open(fn, 'r'))
    sample = vcf_reader.samples[0]
    genotypes = {"bases": [],sample: []}
    for record in vcf_reader:
        if record.CHROM != chrom:
            continue
        genotype = record.genotype(sample)['GT']
        transformed_gt = transform_genotype(genotype)
        if transformed_gt == None:
            continue
        genotypes["bases"].append(record.POS)
        genotypes[sample].append(transformed_gt)
    return pd.DataFrame(genotypes)
        
genotypes = {
    "bases": [],
    "sample": []
}

genotypes = pd.DataFrame(genotypes)

vcf_fofh = open(vcf_fofn,'r')
for fn in vcf_fofh:
    fn = fn.rstrip()
    fn_genotypes = vcf_genotypes(fn)
    genotypes = genotypes.merge(fn_genotypes,how="outer",on="bases") 

genotypes.to_csv(path_or_buf = matrixfn,
                 index = False,
                 sep = "\t")
