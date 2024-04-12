from HLA import HLA
import csv
import sys

### Usage: HLA_check.py path/to/file1.csv path/to/file2.csv method(1 or 2) genes(e.g. A,B,C)

#check that paths to the csv files have been provided as arguments in the command line
assert len(sys.argv) > 4, 'Provide paths to the csv files, matching method [1 or 2] and genes to be matched (e.g. A,B,C)' 
assert sys.argv[3] == '1' or sys.argv[3] == '2', 'Matching method has to be 1 or 2'
file1 = sys.argv[1]
file2 = sys.argv[2]
method = int(sys.argv[3])

#check that the input files have gone through sort_alleles.py first
assert '_sorted.csv' in file1 and '_sorted.csv' in file2, 'Warning: did not detect "sorted_csv" in file names. Input files have to be sorted first using sort_alleles.py'

#create output txt file 
output_file = '' #create txt file name
for path in [file1, file2]:
    file = path.split('/')[-1] #get file name (with _sorted.csv)
    name = '_'.join(file.split('_')[0:-1]) #remove _sorted.csv
    output_file += f'{name}-'
output_file += f'{method}-checked.txt'
f = open(output_file, 'w')
f.write(f"matching method used: {method}\n\n")

#genes that need to be checked:
genes = sys.argv[4]
if genes == 'all': #for ease of use
    genes_list = ['A','B','C','DRB1','DRB3','DRB4','DRB5','DQA1','DQB1','DPB1']
else: genes_list = genes.split(',')
#header that input csv files need to have
header = ['sample_name'] 
for gene in genes_list:
    header.append(f'HLA-{gene}')
    header.append(f'HLA-{gene} (2)')
#genes that need to be checked
hla_genes = []
for gene in genes_list:
    hla_genes.append(f'HLA-{gene}')

print(f'Genes that are being matched: {", ".join(hla_genes)}')
f.write(f'Genes that are being matched: {", ".join(hla_genes)}\n\n')

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

#function that returns lists of hla class opbjects from both files for a specified sample and allele
def get_hla_class(sample, allele):
    #get hla1
    hla = []
    hla_options = output_rows[sample][allele].split('/') #multiple HLA-type options are separated by /
    for option in hla_options:
        if option == '0': hla.append(HLA(None)) #get empty HLA class for 0 allele
        else: hla.append(HLA.from_str(option))
    #get hla2
    hla2 = []
    hla_options = output2_rows[sample][allele].split('/')
    for option in hla_options:
        if option == '0': hla2.append(HLA(None)) #get empty HLA class for 0 allele
        else: hla2.append(HLA.from_str(option))
    return hla, hla2

#function that will test the match between two lists of hla-types
def check_match(hla, hla2, allele_score):
    allele_score_before = allele_score
    for option in hla:
        for option2 in hla2:
            if option.match(option2, method) == True: #use matching method specified in command prompt
                allele_score +=1
    if allele_score == allele_score_before: #if none of the allele options matched, print the no match message
        f.write(output_rows[i]['sample_name'] + ' - ' + allele + ': No match - ' + output_rows[i][allele] + ' vs ' + output2_rows[i][allele] + '\n')
    return allele_score

#check if genes match (assumes alleles are in alfabetical order, use sort_alleles.py first)
gene_score = 0
allele_score = 0
for i in range(0,len(output_rows)):
    for gene in hla_genes:
        alleles = [f'{gene}', f'{gene} (2)']
        for allele in alleles:
            hla, hla2 = get_hla_class(i, allele)
            allele_score = check_match(hla, hla2, allele_score) 
        if allele_score == 2: #if both alleles match
            gene_score += 1
        allele_score = 0
perc_match = round((100*gene_score/(len(output_rows)*len(hla_genes))), 2)
print('Percentage of genes that match: ' + str(perc_match) + '%')
print('see ' + output_file + ' for detailed result')
f.write('\n' + 'Percentage of genes that match: ' + str(perc_match) + '%')