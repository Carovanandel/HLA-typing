import csv

#input file - hla-type.csv
input_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/gefilterd-hla-type.csv'
input_open = open(input_path, 'r', newline='')
input_reader = csv.DictReader(input_open, delimiter=',')

header_full = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/formatted-hla-type.csv'
output_open = open(output_path, 'w', newline='')
output_writer = csv.DictWriter(output_open, fieldnames=header_full)
output_writer.writeheader()

output_row = {column : '' for column in header_full}

for input_row in input_reader:
    output_row['sample_name'] = input_row['sample_name']
    for allele in header_full[1:]:
        genotype = '' #create an empty string
        if input_row[allele] == '0': output_row[allele] = '0'
        else: 
            hla_gene = input_row[allele].split('*')[0] #determine the hla_gene so it can be included in all options
            hla_options = input_row[allele].split('/')
            i = 0
            for option in hla_options:
                if i > 0: genotype += f'/HLA-{hla_gene}*{option}' #options other than the first one don't include the hla gene
                else: genotype += f'HLA-{option}' #the first option does include the hla gene
                i += 1

            output_row[allele] = genotype

    output_writer.writerow(output_row)
    output_row = {column : '' for column in header_full}