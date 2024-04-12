import pandas as pd
import sys

#Usage: sort_alleles.py path/to/input.csv genes(e.g. A,B,C)

#check that a path has been provided as an argument in the command line and genes have been specified
assert len(sys.argv) > 2, 'Provide a path to the input csv file and genes to be sorted (e.g. A,B,C)' 

input_file = sys.argv[1] #use command line argument as the input csv path

df = pd.read_csv(input_file)

#create list of genes that need to be sorted (specified in command prompt)
genes = sys.argv[2]
if genes == 'all': #for ease of use
    genes_list = ['A','B','C','DRB1','DRB3','DRB4','DRB5','DQA1','DQB1','DPB1']
else: genes_list = genes.split(',')
hla_genes = []
for gene in genes_list:
    hla_genes.append(f'HLA-{gene}')

print(f'Genes that are being sorted: {", ".join(hla_genes)}')

#function to sort pairs of alleles
def sort_allele_pair(row):
    for gene in hla_genes:
        alleles = [f'{gene}', f'{gene} (2)']
        row[alleles] = sorted(row[alleles])
    return row

#apply the sorting function to each row (axis=1 > apply row-wise)
df = df.apply(sort_allele_pair, axis=1)

#write the sorted df to an output csv file
output_file = input_file.replace('.csv', '_sorted.csv')
df.to_csv(output_file, index=False)