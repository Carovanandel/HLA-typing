import csv
import json #arcashla output is in .json format

#headers for output csv files
header_T1K = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

header_arcashla = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 
    'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)', 'HLA-DPB1', 'HLA-DPB1 (2)']

header_seq2hla = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']

header_optitype = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)']

header_spechla = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)', 
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)', 'HLA-DPB1', 'HLA-DPB1 (2)']

#create a list of the sample names from the lab output (hla-type.csv)
hla_type_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/full-hla-type.csv'
hla_type = open(hla_type_path, newline='')
hla_type_reader = csv.DictReader(hla_type, fieldnames=header_T1K)

sample_names = []
next(hla_type_reader) #skip header
for row in hla_type_reader:
    sample_names.append(row["sample_name"])

#genes to extract from the sample output files (both with and without HLA- prefix)
genes = ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-DRB1', 'HLA-DRB3', 'HLA-DRB4', 'HLA-DRB5', 'HLA-DQA1', 'HLA-DQB1', 'HLA-DPB1',
         'A', 'B', 'C', 'DRB1', 'DRB3', 'DRB4', 'DRB5', 'DQA1', 'DQB1', 'DPB1']

### Format Seq2HLA ###
#seq2hla combined output file
seq2hla_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/seq2hla-output.csv'
seq2hla_output = open(seq2hla_output_path, 'w', newline='')
seq2hla_output_writer = csv.DictWriter(seq2hla_output, fieldnames=header_seq2hla)
seq2hla_output_writer.writeheader()

#extract genotypes from seq2hla output files
for sample in sample_names:
    output_row_seq2hla = {column: '' for column in header_seq2hla} #create empty output row
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
            output_row_seq2hla['HLA-' + gene + ' (2)'] = f'HLA-{allele2}'
    #get HLA-II genotype
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/seq2hla/{sample}-ClassII.HLAgenotype4digits'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= ['Locus', 'Allele 1', 'Confidence 1', 'Allele 2', 'Confidence 2'])
    for row in sample_reader:
        gene = row['Locus']
        if gene in genes:
            #set allele1 and allele2 variables
            if "'" in row['Allele 1']:  #remove the apostrophe at the end of some of the results
                allele1 = f"HLA-{row['Allele 1'][:-1]}"
            elif "no" in row['Allele 1']: allele1 = '' #'no' alleles need to be empty
            else: allele1 = f"HLA-{row['Allele 1']}" 
            if "'" in row['Allele 2']:
                allele2 = f"HLA-{row['Allele 2'][:-1]}"
            elif "no" in row['Allele 2']: allele2 = ''
            else: allele2 = f"HLA-{row['Allele 2']}"
            output_row_seq2hla['HLA-' + gene] = allele1
            output_row_seq2hla['HLA-' + gene + ' (2)'] = allele2
    seq2hla_output_writer.writerow(output_row_seq2hla)

### Format T1K ###
#t1k combined output file
t1k_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/t1k-output.csv'
t1k_output = open(t1k_output_path, 'w', newline='')
t1k_output_writer = csv.DictWriter(t1k_output, fieldnames=header_T1K)
t1k_output_writer.writeheader()

#function to separate options by '/' - for T1K
def convert_options(genotype):
    if genotype == '0':
        return genotype
    else:
        genotype_options = genotype.split(',')
        return '/'.join(genotype_options)

#extract genotypes from T1K output files and create combined output file
for sample in sample_names:
    output_row_t1k = {column: '' for column in header_T1K} #create empty output row
    output_row_t1k['sample_name'] = sample 
    sample_path = path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/T1K/{sample}_genotype.tsv'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.reader(sample_open, delimiter='\t') #no header in t1k files, so no DictReader possible
    for row in sample_reader:
        gene = row[0]
        if gene in genes:
            if row[2] == '.': output_row_t1k[gene] = '' #no genotype for allele1 > '' in output
            else: output_row_t1k[gene] = convert_options(row[2]) #row[2]: allele 1
            if row[5] == '.': output_row_t1k[gene + ' (2)'] = output_row_t1k[gene] #homozygous > allele 2 = allele 1
            else: output_row_t1k[gene + ' (2)'] = convert_options(row[5]) #row[5]: allele 2
    t1k_output_writer.writerow(output_row_t1k)

### Format OptiType ###
#optitype combined output file
optitype_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/optitype-output.csv'
optitype_output = open(optitype_output_path, 'w', newline='')
optitype_output_writer = csv.DictWriter(optitype_output, fieldnames=header_optitype)
optitype_output_writer.writeheader()

#extract optitype output
for sample in sample_names:
    output_row_optitype = {column: '' for column in header_optitype} #create empty output row
    output_row_optitype['sample_name'] = sample
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/optitype/{sample}.tsv'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= ['x', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)', 'Reads', 'Objective'])
    for row in sample_reader:
        for allele in ['HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)']:
            output_row_optitype[allele] = f'HLA-{row[allele]}'
            # output_row_optitype[allele2] = f'HLA-{row[allele2]}'

    optitype_output_writer.writerow(output_row_optitype)

### Format SpecHLA ###
#spechla combined output file
spechla_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/spechla-output.csv'
spechla_output = open(spechla_output_path, 'w', newline='')
spechla_output_writer = csv.DictWriter(spechla_output, fieldnames=header_spechla)
spechla_output_writer.writeheader()

#create empty output row for spechla
output_row_spechla = {column: '' for column in header_spechla}

#header of spechla output files (order is different in these files)
spechla_fieldnames = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 
                    'HLA-C', 'HLA-C (2)', 'HLA-DPA1', 'HLA-DPA1 (2)', 'HLA-DPB1', 
                    'HLA-DPB1 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)', 
                    'HLA-DRB1', 'HLA-DRB1 (2)']

#extract spechla output
for sample in sample_names:
    output_row_spechla['sample_name'] = sample
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/spechla//hla.result.txt'
    sample_open = open(sample_path, newline='')
    sample_reader = csv.DictReader(sample_open, delimiter='\t', fieldnames= spechla_fieldnames)
    next(sample_reader) #skip database version row
    next(sample_reader) #skip header
    for row in sample_reader:
        for allele in header_spechla[1:]:
            output_row_spechla[allele] = f'HLA-{row[allele]}' #add HLA-prefix
    spechla_output_writer.writerow(output_row_spechla)
    output_row_spechla = {column: '' for column in header_spechla} #clear output row

### Format ArcasHLA ###
#arcashla combined output file
arcashla_output_path = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/arcashla-output.csv'
arcashla_output = open(arcashla_output_path, 'w')
arcashla_output_writer = csv.DictWriter(arcashla_output, fieldnames=header_arcashla)
arcashla_output_writer.writeheader()

#extract arcashla output
for sample in sample_names:
    output_row_arcashla = {column : '' for column in header_arcashla} #create empty output row
    output_row_arcashla['sample_name'] = sample
    sample_path = f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output/{sample}/arcashla/{sample}.genotype.json'
    sample_open = open(sample_path, 'r')
    sample_read = sample_open.read()
    json_sample = json.loads(sample_read) #arcasHLA output is in json format
    for gene in json_sample:
        if gene in genes:
            output_row_arcashla[f'HLA-{gene}'] = f'HLA-{json_sample[gene][0]}' #add HLA-prefix
            output_row_arcashla[f'HLA-{gene} (2)'] = f'HLA-{json_sample[gene][1]}'
    arcashla_output_writer.writerow(output_row_arcashla)