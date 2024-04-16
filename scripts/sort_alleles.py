#!/usr/bin/env python3

import argparse
import pandas as pd
import functools
import sys

def sort_allele_pair(hla_genes, row):
    """Sort pairs of alleles"""
    for gene in hla_genes:
        alleles = [f'{gene}', f'{gene} (2)']
        row[alleles] = sorted(row[alleles])
    return row

def main (input_file, genes, outdir):
    df = pd.read_csv(input_file)

    hla_genes = []
    for gene in genes:
        hla_genes.append(f'HLA-{gene}')

    print(f'Genes that are being sorted: {", ".join(hla_genes)}')

    # Make a temporary function that has hla_genes set
    sorter = functools.partial(sort_allele_pair, hla_genes)
    #apply the sorting function to each row (axis=1 > apply row-wise)
    df = df.apply(sorter, axis=1)

    filename = '.'.join(input_file.split('.')[0:-1]) #remove .csv
    filename = ''.join(filename.split('/')[-1:]) #remove input directory
    outputfilename = f'{filename}_sorted.csv' #add _sorted.csv
    print(outputfilename)
    print(f'{outdir}/{outputfilename}')

    #write the sorted df to an output csv file
    if outdir == sys.stdout:
        df.to_csv(sys.stdout, index=False)
    else: df.to_csv(f'{outdir}/{outputfilename}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input", required=True, help="Input CSV file to be sorted")
    parser.add_argument("--genes", nargs='+', default=['A','B','C','DRB1','DRB3','DRB4','DRB5','DQA1','DQB1','DPB1'], help="Genes to include")
    parser.add_argument("--outdir", default = sys.stdout, help = "Output directory for the sorted csv file")

    args = parser.parse_args()

    main(args.input, args.genes, args.outdir)
