import csv
from HLA import HLA

header_full = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

formatted_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/formatted-hla-type.csv'
formatted_open = open(formatted_path, 'r', newline='')
formatted_reader = csv.DictReader(formatted_open, delimiter=',', fieldnames=header_full)
next(formatted_reader) #skip header

output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/correct-nomen-hla-type.csv'
output_open = open(output_path, 'w', newline='')
output_writer = csv.DictWriter(output_open, delimiter=',', fieldnames=header_full)
output_writer.writeheader()

incorrect_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/incorrect-nomen-hla-type.txt'
incorrect_file = open(incorrect_path, 'w')
incorrect_file.write('Alleles with incorrect nomenclature:\n')

#try to create an hla class for each allele, report errors
for input_row in formatted_reader:
    output_row = {column: '' for column in header_full} #create empty output row
    output_row['sample_name'] = input_row['sample_name']
    for allele in header_full[1:]:
        hla_incorrect = False #variable to check that all options have correct nomenclature
        for option in input_row[allele].split('/'):
            if option != '':
                try: 
                    hla = str(HLA.from_str(option)) #test if hla class can be created, then return string again
                except ValueError: #incorrect nomenclature > hla class cannot be created
                    hla_incorrect = True
        if not hla_incorrect: #only if all options have correct nomenclature, print hla_options
            output_row[allele] = input_row[allele]
        else: 
            output_row[allele] = 'X'
            incorrect_file.write(f'{input_row["sample_name"]} - {input_row[allele]}\n')
    output_writer.writerow(output_row)
