#!/usr/bin/env python3

from HLA import HLA
import csv
import sys
import argparse

def get_hla_list(options):
    """Return a list of hla class objects from a string"""
    hla_list = []
    for option in options.split('/'):
        hla_list.append(HLA(None) if option == '0' else HLA.from_str(option))
    return hla_list
    
def get_hla_class(sample, gene, output_rows, output2_rows):
    """Get lists of hla class objects of both alleles for both files (for given sample+gene)"""
    hla1_1 = get_hla_list(output_rows[sample][gene])
    hla1_2 = get_hla_list(output_rows[sample][f'{gene} (2)'])
    hla2_1 = get_hla_list(output2_rows[sample][gene])
    hla2_2 = get_hla_list(output2_rows[sample][f'{gene} (2)'])
    return hla1_1, hla1_2, hla2_1, hla2_2

def check_match(hla1_1, hla1_2, hla2_1, hla2_2, allele_score, gene, resolution, output_rows, f, i):
    """Test the match of both hla alleles for both files"""
    #variables to prevent double matching, by breaking when a match has already been made (== True)
    hla1_1_match = False
    hla1_2_match = False
    hla2_1_match = False
    hla2_2_match = False
    
    #test the match between hla1_1 and hla2_1
    for option1_1 in hla1_1:
        for option2_1 in hla2_1:
            if hla1_1_match or hla2_1_match: break #break the loop if a match has already been made
            if option1_1.match(option2_1, resolution):
                allele_score += 1 
                hla1_1_match = True
                hla2_1_match = True
    
    #test the match between hla1_2 and hla2_2
    for option1_2 in hla1_2:
        for option2_2 in hla2_2:
            if hla1_2_match or hla2_2_match: break
            if option1_2.match(option2_2, resolution):
                allele_score += 1
                hla1_2_match = True
                hla2_2_match = True

    #test the match between hla1_1 and hla2_2, if hla1_1 has not matched already
    for option1_1 in hla1_1:
        for option2_2 in hla2_2:
            if hla1_1_match or hla2_2_match: break
            if option1_1.match(option2_2, resolution):
                allele_score += 1 
                hla1_1_match = True
                hla2_2_match = True

    #test the match between hla1_2 and hla2_2, if hla1_2 has not matched already
    for option1_2 in hla1_2:
        for option2_1 in hla2_1:
            if hla1_2_match or hla2_1_match: break
            if option1_2.match(option2_1, resolution):
                allele_score += 1 
                hla1_2_match = True
                hla2_1_match = True
    
    #write no match messages to output file
    if hla1_1_match == False:
        if f != sys.stdout:
            f.write(output_rows[i]['sample_name'] + ' - ' + gene + ': no match: ' + str(hla1_1) + ' vs ' + str(hla2_1) +' and ' + str(hla2_2) + '\n')
    if hla1_2_match == False:
        f.write(output_rows[i]['sample_name'] + ' - ' + gene + ': no match: ' + str(hla1_2) + ' vs ' + str(hla2_1) +' and ' + str(hla2_2) + '\n')
    
    return allele_score

def main(input1, input2, resolution, genes, outdir):
    """Create output file, parse hla genes and headers, read input files, match hla alleles, calculate allele score"""
    #create output txt file 
    output_file = '' #create txt file name
    for path in [input1, input2]:
        file = path.split('/')[-1] #get file name
        name = '.'.join(file.split('.')[0:-1]) #remove .csv
        output_file += f'{name}-'
    output_file += f'{resolution}-checked.txt'
    if outdir == sys.stdout:
        f = sys.stdout
    else: 
        if outdir[-1:] == '/': outdir = outdir[:-1] #remove / from end of outdir if present
        f = open(f'{outdir}/{output_file}', 'w')
    f.write(f"matching resolution used: {resolution}\n\n")

    #parse genes that need to be checked
    hla_genes = []
    for gene in genes:
        hla_genes.append(f'HLA-{gene}')
    #create header
    header = ['sample_name'] 
    for gene in genes:
        header.append(f'HLA-{gene}')
        header.append(f'HLA-{gene} (2)')

    if f != sys.stdout: print(f'Genes that are being matched: {", ".join(hla_genes)}')
    f.write(f'Genes that are being matched: {", ".join(hla_genes)}\n\n')

    #read input files
    input_rows = []
    for file in [input1, input2]:
        open_file = open(file, newline='')
        reader_file = csv.DictReader(open_file, fieldnames=header)
        next(reader_file) #skip header
        input_rows.append(list(reader_file))
    output_rows = input_rows[0]
    output2_rows = input_rows[1]

    #check both csv files have the same amount of samples
    assert len(output_rows) == len(output2_rows), "csv files have different amount of samples"

    #check if hla-types match and calculate percentage of correct alleles
    allele_score = 0
    for i in range(0,len(output_rows)):
        for gene in hla_genes:
            hla1_1, hla1_2, hla2_1, hla2_2 = get_hla_class(i, gene, output_rows, output2_rows)
            allele_score = check_match(hla1_1, hla1_2, hla2_1, hla2_2, allele_score, gene, resolution, output_rows, f, i)

    perc_match = round((100*allele_score/(len(output_rows)*len(hla_genes)*2)), 2)
    if f != sys.stdout:
        print('Percentage of alleles that match: ' + str(perc_match) + '%' + '\nsee ' + outdir + '/' + output_file + ' for detailed result')
    f.write('\nPercentage of alleles that match: ' + str(perc_match) + '%\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input1", required=True, help="Input 1 CSV file to be matched")
    parser.add_argument("--input2", required=True, help="Input 2 CSV file to be matched")
    parser.add_argument("--resolution", default=None, help="Resolution at which matching should be done")
    parser.add_argument("--genes", nargs='+', default=['A','B','C','DRB1','DRB3','DRB4','DRB5','DQA1','DQB1','DPB1'], help="Genes to include")
    parser.add_argument("--outdir", default = sys.stdout, help = "Output directory for the matching result")

    args = parser.parse_args()

    main(args.input1, args.input2, args.resolution, args.genes, args.outdir)