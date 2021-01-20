#!/bin/env python
import sys
import pandas as pd

matrixfn = sys.argv[1]
outfn = sys.argv[2]

matrix = pd.read_csv(matrixfn,sep="\t",index_col=False,header=None)
matrix = matrix.T
matrix.to_csv(outfn,index=False,sep="\t",header=False)
