from HLA import HLA
import csv
import sys

### Usage: HLA_check.py path/to/file1.csv path/to/file2.csv method(1 or 2) [optional: add 'mini' argument for only HLA-A tests]

#check that paths to the csv files have been provided as arguments in the command line
assert len(sys.argv) > 3, 'Provide paths to the csv files and matching method [1 (identical) or 2 (resolution ambiguity allowed)]' 
file1 = sys.argv[1]
file2 = sys.argv[2]
method = int(sys.argv[3])

#create output txt file name
output_file = ''
for path in [file1, file2]:
    file = path.split('/')[-1] #get file name (with _sorted.csv)
    name = '_'.join(file.split('_')[0:-1]) #remove _sorted.csv
    output_file += f'{name}-'
output_file += f'{method}-checked.txt'

f = open(output_file, 'w')
f.write(f"matching method used: {method}\n\n")

#header that the csv files need to have:
if len(sys.argv) > 4: #if the optional extra argument (mini) has been added, check only HLA-A 
    header = ['sample_name', 'HLA-A', 'HLA-A (2)']
    print('Attention: using mini version, only HLA-A is being matched')
    f.write('Attention: using mini version, only HLA-A is being matched'+'\n \n')
else:
    header = ['sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
        'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
        'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
        'HLA-DPB1', 'HLA-DPB1 (2)']

#csv file 1
path_test = file1
open_test = open(path_test, newline='')
reader_test = csv.DictReader(open_test, fieldnames=header)
next(reader_test) #skip header

#csv file 2
path_test2 = file2
open_test2 = open(path_test2, newline='')
reader_test2 = csv.DictReader(open_test2, fieldnames=header)
next(reader_test2) #skip header

output_rows = list(reader_test)
output2_rows = list(reader_test2)

#check both csv files have the same amount of samples
assert len(output_rows) == len(output2_rows), "csv files have different amount of samples"

#genes that need to be checked
if len(sys.argv) > 4: #if the optional extra argument (mini) has been added, check only HLA-A 
    hla_genes = ['HLA-A']
else: 
    hla_genes = ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-DRB1', 'HLA-DRB3', 'HLA-DRB4',
                'HLA-DRB5', 'HLA-DQA1', 'HLA-DQB1', 'HLA-DPB1'] 

#check if genes match (assumes alleles are in alfabetical order, use sort_alleles.py first)
gene_score = 0
allele_score = 0
for i in range(0,len(output_rows)):
    for gene in hla_genes:
        alleles = [f'{gene}', f'{gene} (2)']
        for allele in alleles:
            hla = HLA.from_str(output_rows[i][allele])
            hla2 = HLA.from_str(output2_rows[i][allele])
            #if there are multiple allele options in the lab result, hla will be a list of hla class objects
            if isinstance(hla, list):
                allele_score_before = allele_score
                for option in hla:
                    if option.match(hla2, method) == True: #use matching method specified in command prompt
                        allele_score +=1
                if allele_score == allele_score_before: #if none of the allele options matched, print the no match message
                    f.write(output_rows[i]['sample_name'] + ' - ' + allele + ': No match - ' + output_rows[i][allele] + ' vs ' + output2_rows[i][allele] + '\n')
            #if the lab result only gives one allele option, hla will be one hla class object
            else:
                if hla.match(hla2, method) == True: #use matching method specified in command prompt
                    allele_score += 1
                else: f.write(output_rows[i]['sample_name'] + ' - ' + allele + ': No match - ' + output_rows[i][allele] + ' vs ' + output2_rows[i][allele] + '\n')
        if allele_score == 2: #if both alleles match
            gene_score += 1
        allele_score = 0
perc_match = round((100*gene_score/(len(output_rows)*len(hla_genes))), 2)
print('Percentage of genes that match: ' + str(perc_match) + '%')
print('see ' + output_file + ' for detailed result')
f.write('\n' + 'Percentage of genes that match: ' + str(perc_match) + '%')