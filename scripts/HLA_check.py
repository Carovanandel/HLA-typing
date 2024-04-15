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

#create output txt file 
output_file = '' #create txt file name
for path in [file1, file2]:
    file = path.split('/')[-1] #get file name (with _sorted.csv)
    name = '.'.join(file.split('.')[0:-1]) #.csv
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

#function that returns a list of hla class objects from a string
def list_to_hla(options):
    for option in options.split('/'):
        return [HLA(None) if option == '0' else HLA.from_str(option)]
    
#function that uses list_to_hla to get hla class lists of both alleles for both files
def get_hla_class(sample, gene):
    hla1_1 = list_to_hla(output_rows[sample][gene])
    hla1_2 = list_to_hla(output_rows[sample][f'{gene} (2)'])
    hla2_1 = list_to_hla(output2_rows[sample][gene])
    hla2_2 = list_to_hla(output2_rows[sample][f'{gene} (2)'])
    return hla1_1, hla1_2, hla2_1, hla2_2

#function that will test the match of hla alleles
def check_match(hla1_1, hla1_2, hla2_1, hla2_2, allele_score):
    hla1_1_match = False
    hla1_2_match = False
    
    #test the match between hla1_1 and hla2_1
    for option1_1 in hla1_1:
        for option2_1 in hla2_1:
            if hla1_1_match: break #break the loop if a match has already been made
            if option1_1.match(option2_1, method):
                allele_score += 1 
                hla1_1_match = True
    
    #test the match between hla1_2 and hla2_2
    for option1_2 in hla1_2:
        for option2_2 in hla2_2:
            if hla1_2_match: break
            if option1_2.match(option2_2, method):
                allele_score += 1
                hla1_2_match = True

    #test the match between hla1_1 and hla2_2, if hla1_1 has not matched already
    for option1_1 in hla1_1:
        for option2_2 in hla2_2:
            if hla1_1_match: break
            if option1_1.match(option2_2, method):
                allele_score += 1 
                hla1_1_match = True

    #test the match between hla1_2 and hla2_2, if hla1_2 has not matched already
    for option1_2 in hla1_2:
        for option2_1 in hla2_1:
            if hla1_2_match: break
            if option1_2.match(option2_1, method):
                allele_score += 1 
                hla1_2_match = True
    
    #write no match messages to output file
    if hla1_1_match == False:
        f.write(output_rows[i]['sample_name'] + ' - ' + gene + ': no match: ' + str(hla1_1) + ' vs ' + str(hla2_1) +' and ' + str(hla2_2) + '\n')
    if hla1_2_match == False:
        f.write(output_rows[i]['sample_name'] + ' - ' + gene + ': no match: ' + str(hla1_2) + ' vs ' + str(hla2_1) +' and ' + str(hla2_2) + '\n')
    
    return allele_score

#check if hla-types match and calculate percentage of correct alleles
allele_score = 0
for i in range(0,len(output_rows)):
    for gene in hla_genes:
        hla1_1, hla1_2, hla2_1, hla2_2 = get_hla_class(i, gene)
        allele_score = check_match(hla1_1, hla1_2, hla2_1, hla2_2, allele_score)

perc_match = round((100*allele_score/(len(output_rows)*len(hla_genes)*2)), 2)
print('Percentage of alleles that match: ' + str(perc_match) + '%')
print('see ' + output_file + ' for detailed result')
f.write('\n\n' + 'Percentage of alleles that match: ' + str(perc_match) + '%')