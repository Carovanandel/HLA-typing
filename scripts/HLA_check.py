from HLA import HLA
import csv
import sys

### Usage: HLA_check.py path/to/file1.csv path/to/file2.csv

#check that paths to the csv files have been provided as arguments in the command line
assert len(sys.argv) > 2, 'Provide paths to the csv files' 
file1 = sys.argv[1]
file2 = sys.argv[2]

#test_output.csv
path_test = file1
open_test = open(path_test, newline='')
reader_test = csv.DictReader(open_test, fieldnames=["sample_name","HLA-A","HLA-A (2)"])
next(reader_test) #skip header

#test_output2.csv
path_test2 = file2
open_test2 = open(path_test2, newline='')
reader_test2 = csv.DictReader(open_test2, fieldnames=["sample_name","HLA-A","HLA-A (2)"])
next(reader_test2) #skip header

output_rows = list(reader_test)
output2_rows = list(reader_test2)

#check both csv files have the same amount of samples
assert len(output_rows) == len(output2_rows), "csv files have different amount of samples"

#check if alleles are identical (assumes alleles are in alfabetical order, use sort_alleles.py first)
alleles = ["HLA-A", "HLA-A (2)"]
allele_score = 0
for i in range(0,len(output_rows)):
    for allele in alleles:
        if HLA.from_str(output_rows[i][allele]) == HLA.from_str(output2_rows[i][allele]): 
            print(output_rows[i]["sample_name"] + " - " + allele + ": Identical") 
            allele_score += 1
        else: print(output_rows[i]["sample_name"] + " - " + allele + ": Not identical")
print("Percentage of alleles identical: " + str(100*allele_score/(len(output_rows)*len(alleles))) + "%")