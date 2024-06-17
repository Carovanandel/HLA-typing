import csv

### Use this script to parse the lab output into the correct format

#input file - hla-type.csv
input_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/raw-hla-type.csv'
input_open = open(input_path, 'r', newline='')
input_reader = csv.DictReader(input_open, delimiter=',')

header_full = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/formatted-hla-type.csv'
output_open = open(output_path, 'w', newline='')
output_writer = csv.DictWriter(output_open, fieldnames=header_full)
output_writer.writeheader()

def format_options(input_row, allele):
    genotype = '' #create an empty string for the formatted genotype
    hla_gene = input_row[allele].split('*')[0] #determine the hla gene so it can be included in all options for correct nomenclature
    i = 0
    for option in input_row[allele].split('/'): #split multiple genotype options
        if i == 0: genotype += f'HLA-{option}' #the first option already includes the hla gene
        else: genotype += f'/HLA-{hla_gene}*{option}' #add the hla gene to all other options
        i +=1
    
    return genotype

for input_row in input_reader:
    output_row = {column : '' for column in header_full} #create empty output row
    output_row['sample_name'] = input_row['sample_name']
    for allele in ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-DRB1', 'HLA-DRB3', 'HLA-DRB4', 'HLA-DRB5', 'HLA-DQA1',
                   'HLA-DQB1', 'HLA-DPB1']:
        allele2 = f'{allele} (2)'
        if input_row[allele] == '0': output_row[allele] = '' # no genotype > put ''
        else: output_row[allele] = format_options(input_row, allele)
        if input_row[allele2] == '0': output_row[allele2] = output_row[allele] #homozygous > same as allele 1
        else: output_row[allele2] = format_options(input_row, allele2)

    output_writer.writerow(output_row)