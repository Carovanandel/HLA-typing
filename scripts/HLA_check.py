from HLA import HLA
import csv
import sys

### Usage: HLA_check.py path/to/file1.csv path/to/file2.csv method(1 or 2) [optional: add 'mini' argument for only HLA-A tests]

#check that paths to the csv files have been provided as arguments in the command line
assert len(sys.argv) > 3, 'Provide paths to the csv files and matching method [1 (identical) or 2 (resolution ambiguity allowed)]' 
file1 = sys.argv[1]
file2 = sys.argv[2]
method = sys.argv[3]

#create output txt file name
output_file = ''
for path in [file1, file2]:
    file = path.split('/')[-1] #get file name (with _sorted.csv)
    name = '_'.join(file.split('_')[0:-1]) #remove _sorted.csv
    output_file += f"{name}-"
output_file += 'checked.txt'

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

#Alleles that need to be checked
if len(sys.argv) > 4: #if the optional extra argument (mini) has been added, check only HLA-A 
    alleles = ['HLA-A', 'HLA-A (2)']
else:
    alleles = ['HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
        'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
        'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
        'HLA-DPB1', 'HLA-DPB1 (2)']

#check if alleles match (assumes alleles are in alfabetical order, use sort_alleles.py first)
allele_score = 0
for i in range(0,len(output_rows)):
    for allele in alleles:
        #print(allele) #for debugging
        hla = HLA.from_str(output_rows[i][allele])
        hla2 = HLA.from_str(output2_rows[i][allele])
        if hla.match(hla2, 2) == True: #use matching method 2 to allow resolution differences
            allele_score += 1
        else: f.write(output_rows[i]['sample_name'] + ' - ' + allele + ': Not identical - ' + output_rows[i][allele] + ' vs ' + output2_rows[i][allele] + '\n')
#calculate percentage of alleles identical and round the percentage to 2 digits
perc_identical = round((100*allele_score/(len(output_rows)*len(alleles))), 2)
print('Percentage of alleles identical: ' + str(perc_identical) + '%')
print('see ' + output_file + ' for detailed result')
f.write('\n' + 'Percentage of alleles identical: ' + str(perc_identical) + '%')