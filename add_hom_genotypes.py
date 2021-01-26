#!/bin/env python
import sys
import vcf
import pysam
from collections import namedtuple

vcffn = sys.argv[1]
bamfn = sys.argv[2]
reffn = sys.argv[3]
outvcffn = sys.argv[4]
sample_name = sys.argv[5]

def read_vcf(vcffn):
    snps = {}
    vcf_reader = vcf.Reader(open(vcffn, 'r'))
    for record in vcf_reader:
        if record.CHROM != "igh":
            continue
        snps[record.POS] = record
    #vcf_reader.close()
    return snps

def get_hom_record(ref,pos,sample_name):
    refbase = ref.fetch("igh",pileupcolumn.pos - 1,pileupcolumn.pos).upper()
    record_to_add = vcf.model._Record("igh",pileupcolumn.pos,".",refbase,[None],60,"PASS",{},"GT",[])
    sample_data = data("0/0")
    sample = vcf.model._Call(record_to_add,sample_name,sample_data)
    record_to_add.samples = [sample]
    return record_to_add

snps = read_vcf(vcffn)

old_vcf = vcf.Reader(open(vcffn, 'r'))
new_vcf = vcf.Writer(open(outvcffn,'w'), old_vcf)

samfile = pysam.AlignmentFile(bamfn,'r')
ref = pysam.FastaFile(reffn)

data = namedtuple('data',['GT'])

for pileupcolumn in samfile.pileup("igh", 1, 1194129):
    if pileupcolumn.n < 20:
        continue
    if pileupcolumn.pos in snps:
        new_vcf.write_record(snps[pileupcolumn.pos])
        continue
    record_to_add = get_hom_record(ref,pileupcolumn.pos,sample_name)
    new_vcf.write_record(record_to_add)

