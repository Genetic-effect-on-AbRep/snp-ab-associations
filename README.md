# snp-ab-associations
## Merge usage matrices
```
python merge_matrix.py matrix.fofn names.fofn matrix_merged.txt
```

## VCFs to genotype matrix 
```
python snp_vcfs_to_matrix.py vcfs.fofn vcf_matrix.txt
```

## Format for [Matrix eQTL](http://www.bios.unc.edu/research/genomic_software/Matrix_eQTL/)
```
python prep_datasets.py matrix_merged.txt vcf_matrix.txt outdir names.txt
```

## Run [Matrix eQTL](http://www.bios.unc.edu/research/genomic_software/Matrix_eQTL/)
```
Rscript run_matrix_eqtl.R outdir/snp.txt outdir/gene.txt cov.txt qtl.txt
```
