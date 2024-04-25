import csv
import json #arcashla output is in .json format

#headers for output csv files
#header_full: all 10 genes in lab result - for T1K and arcasHLA
header_full = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

header_seq2hla = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

header_optitype = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)']

header_spechla = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)', 
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)', 'HLA-DPB1', 'HLA-DPB1 (2)']

#create a list of the sample names from the lab output (hla-type.csv)
hla_type_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/gefilterd-hla-type.csv'
hla_type = open(hla_type_path, newline='')
hla_type_reader = csv.DictReader(hla_type, fieldnames=header_full)

sample_names = []
next(hla_type_reader) #skip header
for row in hla_type_reader:
    sample_names.append(row["sample_name"])

#genes to extract from the sample output files (both with and without HLA- prefix)
genes = ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-DRB1', 'HLA-DRB3', 'HLA-DRB4', 'HLA-DRB5', 'HLA-DQA1', 'HLA-DQB1', 'HLA-DPB1',
         'A', 'B', 'C', 'DRB1', 'DRB3', 'DRB4', 'DRB5', 'DQA1', 'DQB1', 'DPB1']

### Format Seq2HLA ###
#seq2hla combined output file
seq2hla_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/seq2hla-output.csv'
seq2hla_output = open(seq2hla_output_path, 'w', newline='')
seq2hla_output_writer = csv.DictWriter(seq2hla_output, fieldnames=header_seq2hla)
seq2hla_output_writer.writeheader()

#create empty output row for seq2hla
output_row_seq2hla = {column: '' for column in header_seq2hla}

#extract genotypes from seq2hla output files
for sample in sample_names:
    output_row_seq2hla['sample_name'] = sample
    #get HLA-I genotype
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/seq2hla/{sample}-ClassI-class.HLAgenotype4digits'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= ['Locus', 'Allele 1', 'Confidence 1', 'Allele 2', 'Confidence 2'])
    for row in sample_reader:
        gene = row['Locus']
        if gene in genes:
             #set allele1 and allele2 variables
            if "'" in row['Allele 1']:  #remove the apostrophe at the end of some of the results
                allele1 = row['Allele 1'][:-1]
            else: allele1 = row['Allele 1']
            if "'" in row['Allele 2']:
                allele2 = row['Allele 2'][:-1]
            else: allele2 = row['Allele 2']
            #write alleles to output-row
            output_row_seq2hla['HLA-' + gene] = f'HLA-{allele1}'
            if allele1 == allele2:  #homozygous > put 0 for second allele
                output_row_seq2hla['HLA-' + gene + ' (2)'] = '0'
            else: output_row_seq2hla['HLA-' + gene + ' (2)'] = f'HLA-{allele2}'
    #get HLA-II genotype
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/seq2hla/{sample}-ClassII.HLAgenotype4digits'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= ['Locus', 'Allele 1', 'Confidence 1', 'Allele 2', 'Confidence 2'])
    for row in sample_reader:
        gene = row['Locus']
        if gene in genes:
            #set allele1 and allele2 variables
            if "'" in row['Allele 1']:  #remove the apostrophe at the end of some of the results
                allele1 = row['Allele 1'][:-1]
            else: allele1 = row['Allele 1']
            if "'" in row['Allele 2']:
                allele2 = row['Allele 2'][:-1]
            else: allele2 = row['Allele 2']
            output_row_seq2hla['HLA-' + gene] = f'HLA-{allele1}'
            if allele1 == allele2:  #homozygous > put 0 for second allele
                output_row_seq2hla['HLA-' + gene + ' (2)'] = '0'
            else: output_row_seq2hla['HLA-' + gene + ' (2)'] = f'HLA-{allele2}'
    seq2hla_output_writer.writerow(output_row_seq2hla)
    output_row = {column: '' for column in header_seq2hla} #clear output row

### Format T1K ###
#t1k combined output file
t1k_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/t1k-output.csv'
t1k_output = open(t1k_output_path, 'w', newline='')
t1k_output_writer = csv.DictWriter(t1k_output, fieldnames=header_full)
t1k_output_writer.writeheader()

#create empty output rows for T1K
output_row_t1k = {column: '' for column in header_full}

#function to separate options by '/' - for T1K
def convert_options(genotype):
    if genotype == '0':
        return genotype
    else:
        genotype_options = genotype.split(',')
        return '/'.join(genotype_options)

#extract genotypes from T1K output files and create combined output file
for sample in sample_names:
    output_row_t1k['sample_name'] = sample 
    sample_path = path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/T1K/{sample}_genotype.tsv'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.reader(sample_open, delimiter='\t') #no header in t1k files, so no DictReader possible
    for row in sample_reader:
        gene = row[0]
        if gene in genes:
            if row[1] == '2': #row[1]: num of alleles
                output_row_t1k[gene] = convert_options(row[2]) #row[2]: allele 1
                output_row_t1k[gene + ' (2)'] = convert_options(row[5]) #row[5]: allele 2
            elif row[1] == '1':
                output_row_t1k[gene] = convert_options(row[2])
                output_row_t1k[gene + ' (2)'] = '0'
            else:
                output_row_t1k[gene] = '0'
                output_row_t1k[gene + ' (2)'] = '0'
    t1k_output_writer.writerow(output_row_t1k)

    output_row_t1k = {column: '' for column in header_full} #clear output row

### Format OptiType ###
#optitype combined output file
optitype_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/optitype-output.csv'
optitype_output = open(optitype_output_path, 'w', newline='')
optitype_output_writer = csv.DictWriter(optitype_output, fieldnames=header_optitype)
optitype_output_writer.writeheader()

#create empty output row for optitype
output_row_optitype = {column: '' for column in header_optitype}

#extract optitype output
for sample in sample_names:
    output_row_optitype['sample_name'] = sample
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/optitype/{sample}.tsv'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= ['x', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)', 'Reads', 'Objective'])
    for row in sample_reader:
        for allele in ['HLA-A', 'HLA-B', 'HLA-C']:
            allele2 = f'{allele} (2)'
            if row[allele] == row[allele2]: #homozygous > put 0 for second allele
                output_row_optitype[allele] = f'HLA-{row[allele]}' #add HLA-prefix
                output_row_optitype[allele2] = '0'
            else:
                output_row_optitype[allele] = f'HLA-{row[allele]}'
                output_row_optitype[allele2] = f'HLA-{row[allele2]}'

    optitype_output_writer.writerow(output_row_optitype)
    output_row_optitype = {column: '' for column in header_optitype}  #clear output row

### Format SpecHLA ###
#spechla combined output file
spechla_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-analysis/spechla-output.csv'
spechla_output = open(spechla_output_path, 'w', newline='')
spechla_output_writer = csv.DictWriter(spechla_output, fieldnames=header_spechla)
spechla_output_writer.writeheader()

#create empty output row for spechla
output_row_spechla = {column: '' for column in header_spechla}

#header of spechla output files
spechla_fieldnames = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 
                    'HLA-C', 'HLA-C (2)', 'HLA-DPA1', 'HLA-DPA1 (2)', 'HLA-DPB1', 
                    'HLA-DPB1 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)', 
                    'HLA-DRB1', 'HLA-DRB1 (2)']

#extract spechla output
for sample in ['102581-002-004', '102581-002-006', '102581-002-007', '102581-002-010', '102581-002-014']: #only first 5 samples have been analyzed so far
    output_row_spechla['sample_name'] = sample
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/spechla/{sample}/hla.result.txt'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= spechla_fieldnames)
    next(sample_reader) #skip database version row
    next(sample_reader) #skip header
    for row in sample_reader:
            for allele in ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-DPB1', 'HLA-DQA1', 'HLA-DQB1', 'HLA-DRB1']:
                allele2 = f'{allele} (2)'
                output_row_spechla[allele] = f'HLA-{row[allele]}' #add HLA-prefix
                if row[allele] == row[allele2]: #homozygous at 3-field > put 0 for second allele
                    output_row_spechla[allele2] = '0'
                else: output_row_spechla[allele2] = f'HLA-{row[allele2]}'
    spechla_output_writer.writerow(output_row_spechla)
    output_row_spechla = {column: '' for column in header_spechla} #clear output row

### Format ArcasHLA ###
#arcashla combined output file
arcashla_output_path = 'output-analysis/arcashla-output.csv'
arcashla_output = open(arcashla_output_path, 'w')
arcashla_output_writer = csv.DictWriter(arcashla_output, fieldnames=header_full)
arcashla_output_writer.writeheader()

#create empty output row for arcashla (genes without result are missing, so 0's have to be the standard value)
output_row = {column : '0' for column in header_full}

#extract arcashla output
for sample in ['102581-002-004', '102581-002-006', '102581-002-007', '102581-002-010', '102581-002-014']: #only first 5 samples have been analyzed so far
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/arcashla/{sample}.genotype.json'
    sample_open = open(sample_path, 'r')
    sample_read = sample_open.read()
    json_sample = json.loads(sample_read)
    for gene in json_sample:
        if gene in genes:
            output_row[f'HLA-{gene}'] = f'HLA-{json_sample[gene][0]}'
            if json_sample[gene][0] != json_sample[gene][1]: 
                output_row[f'HLA-{gene} (2)'] = f'HLA-{json_sample[gene][1]}'
    output_row['sample_name'] = sample
    arcashla_output_writer.writerow(output_row)
    output_row = {column : '0' for column in header_full}