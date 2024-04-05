import pandas as pd
import sys

#Usage: sort_alleles.py path/to/input.csv

#check that a path has been provided as an argument in the command line
assert len(sys.argv) > 1, 'Provide a path to the input csv file' 

input_file = sys.argv[1] #use command line argument as the input csv path

df = pd.read_csv(input_file)

#function to sort pairs of alleles
def sort_allele_pair(row):
    hla_genes = ['HLA-A']  #add more HLA genes here
    for gene in hla_genes:
        alleles = [f'{gene}', f'{gene} (2)']
        row[alleles] = sorted(row[alleles])
    return row

#apply the sorting function to each row (axis=1 > apply row-wise)
df = df.apply(sort_allele_pair, axis=1)

#write the sorted df to an output csv file
output_file = input_file.replace('.csv', '_sorted.csv')
df.to_csv(output_file, index=False)