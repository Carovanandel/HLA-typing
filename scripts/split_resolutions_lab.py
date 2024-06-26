import csv
from HLA import HLA

### Use this script to create lab output files with HLA types of more than 2 and more than 3 resolution fields, 
### used by get_results.py to calculate accuracy at these resolutions

header_full = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

lab_hla_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/full-hla-type.csv'
lab_hla_open = open(lab_hla_path, 'r', newline='')
lab_hla_reader = csv.DictReader(lab_hla_open, delimiter=',', fieldnames=header_full)
next(lab_hla_reader) #skip header

output2_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/2-fields-hla-type.csv'
output2_open = open(output2_path, 'w', newline='')
output2_writer = csv.DictWriter(output2_open, delimiter=',', fieldnames=header_full)
output2_writer.writeheader()

output3_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/3-fields-hla-type.csv'
output3_open = open(output3_path, 'w', newline='')
output3_writer = csv.DictWriter(output3_open, delimiter=',', fieldnames=header_full)
output3_writer.writeheader()

for input_row in lab_hla_reader:
    output2_row = {column: '' for column in header_full} #create empty output row
    output2_row['sample_name'] = input_row['sample_name']
    output3_row = {column: '' for column in header_full}
    output3_row['sample_name'] = input_row['sample_name']
    for allele in header_full[1:]:
        lower_than_2 = False #variables to check that all options have a sufficient resolution
        lower_than_3 = False
        for option in input_row[allele].split('/'):
            if option != 'X' and option != '': #skip 'X' and '' genotypes
                hla = HLA.from_str(option)
                if hla.fields()[2] == None:
                    lower_than_2 = True
                    lower_than_3 = True
                elif hla.fields()[3] == None:
                    lower_than_3 = True
        if lower_than_2 and lower_than_3: #lower than 2 fields resolution > remove allele from both 2- and 3-fields output
            output2_row[allele] = ''
            output3_row[allele] = ''
        elif not lower_than_2 and lower_than_3: #2 fields resolution > remove allele in 3-fields output, but leave in 2-fields output
            output2_row[allele] = input_row[allele]
            output3_row[allele] = ''
        else: #3 fields or higher resolution > leave genotype in both 2- and 3-field output
            output2_row[allele] = input_row[allele]
            output3_row[allele] = input_row[allele]
    output2_writer.writerow(output2_row)
    output3_writer.writerow(output3_row)