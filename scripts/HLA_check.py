from HLA import HLA
import csv
import sys

### Usage: HLA_check.py path/to/file1.csv path/to/file2.csv

#check that paths to the csv files have been provided as arguments in the command line
assert len(sys.argv) > 2, 'Provide paths to the csv files' 
file1 = sys.argv[1]
file2 = sys.argv[2]

#Header that the csv files need to have:
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

#check if alleles match (assumes alleles are in alfabetical order, use sort_alleles.py first)
alleles = ['HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', 'HLA-C', 'HLA-C (2)',
    'HLA-DRB1', 'HLA-DRB1 (2)', 'HLA-DRB3', 'HLA-DRB3 (2)', 'HLA-DRB4', 'HLA-DRB4 (2)',
    'HLA-DRB5', 'HLA-DRB5 (2)', 'HLA-DQA1', 'HLA-DQA1 (2)', 'HLA-DQB1', 'HLA-DQB1 (2)',
    'HLA-DPB1', 'HLA-DPB1 (2)']
allele_score = 0
for i in range(0,len(output_rows)):
    for allele in alleles:
        #print(allele) #for debugging
        hla = HLA.from_str(output_rows[i][allele])
        hla2 = HLA.from_str(output2_rows[i][allele])
        if hla.match(hla2, 2) == True: #use matching method 2 to allow resolution differences
            allele_score += 1
        else: print(output_rows[i]["sample_name"] + " - " + allele + ": Not identical - " + output_rows[i][allele] + " vs " + output2_rows[i][allele])
#calculate percentage of alleles identical and round the percentage to 2 digits
perc_identical = round((100*allele_score/(len(output_rows)*len(alleles))), 2)
print("Percentage of alleles identical: " + str(perc_identical) + "%")