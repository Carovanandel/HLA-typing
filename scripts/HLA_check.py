#!/usr/bin/env python3

from HLA import HLA
import csv
import sys
import argparse

def get_hla_list(options):
    """Return a list of hla class objects from a string, and the alelle validity"""
    hla_list = []
    #optional: support for 'X' (incorrect nomenclature)
    # if options == 'X': 
    #     hla_list = [HLA('X')]
    #     allele_validity = 'inc_nomen'
    if options == '':
        hla_list = [HLA('empty')]
        allele_validity = 'empty' #empty allele
    else:
        allele_validity = 'valid' #valid allele
        options_sorted = sorted(options.split('/')) #sort options alphabetically, necessary for 'all' match method
        for option in options_sorted:
            hla_list.append(HLA.from_str(option))
    return hla_list, allele_validity
    
def get_hla_class(sample, gene, input1_rows, input2_rows):
    """Get lists of hla class objects of both alleles for both files (for given sample+gene)"""
    hla1_1, allele_validity1_1 = get_hla_list(input1_rows[sample][gene])
    hla1_2, allele_validity1_2 = get_hla_list(input1_rows[sample][f'{gene} (2)'])
    hla2_1, allele_validity2_1 = get_hla_list(input2_rows[sample][gene])
    hla2_2, allele_validity2_2 = get_hla_list(input2_rows[sample][f'{gene} (2)'])
    
    count_empty = max(sum([allele_validity1_1 == 'empty', allele_validity1_2 == 'empty']), 
                  sum([allele_validity2_1 == 'empty', allele_validity2_2 == 'empty']))
    count_valid = 2 - count_empty

    return hla1_1, hla1_2, hla2_1, hla2_2, [count_valid, count_empty]

def check_match(hla1, hla2, resolution, method):
    """Test the match between two hla lists, for a given resolution and method"""
    if hla1 == [HLA('empty')] and hla2 == [HLA('empty')]: return False #both empty alleles ('' alleles) > return false (alleles are excluded)
    if hla1 == [HLA('X')] and hla2 == [HLA('X')]: return False #both inc_nomen alleles > return false (alleles are excluded)
    if method == 'any':
        for option1 in hla1:
            for option2 in hla2:
                if option1.match(option2, resolution): return True #if any option matches, return True
        return False #if no options match, return False
    if method == 'all':
        if len(hla1) != len(hla2): return False #if one list has more options than the other, return False
        #hla1 and hla2 have been sorted alphabetically by get_hla_list()
        for i in range(len(hla1)):
            if not hla1[i].match(hla2[i], resolution): return False #if any option does not match, return False
        return True #if all options match, return True
    
def match_pairs(hla1_1, hla1_2, hla2_1, hla2_2, resolution, method):
    """Get the allele score for both combinations of allele matches and return the highest score"""
    combinations = [
        [(hla1_1, hla2_1), (hla1_2, hla2_2)],
        [(hla1_1, hla2_2), (hla1_2, hla2_1)]
    ]
    max_score = 0
    pair_nr = 1 #variable to note which pair is being matched
    matched_pairs = [] #list to note pairs that matched successfully for printing a mismatch message
    for option in combinations:
        score = 0
        for pair in option:
            if check_match(pair[0], pair[1], resolution, method): 
                score += 1
                matched_pairs.append(pair_nr)
                #debugging - print matches:
                #print(f'match: {pair[0]} and {pair[1]}')
            pair_nr += 1
        max_score = max(max_score, score)
    
    #dubgging - print matched pairs and score
    #print(f'score: {max_score}, matched_pairs: {matched_pairs}')
    return max_score, matched_pairs

def mismatch_message(f, input1_rows, i, gene, score, matched_pairs, hla1_1, hla1_2, hla2_1, hla2_2):
    """Print a mismatch message to the output file"""
    if score == 0: #both alleles did not match
        if [HLA('empty')] in (hla1_1, hla1_2, hla2_1, hla2_2):
            return #no mismatch message for empty alleles
        elif [HLA('X')] in (hla1_1, hla2_1) and [HLA('X')] in (hla1_2, hla2_2):
            return #no mismatch message if both alleles have incorrect nomenclature
        elif [HLA('X')] in (hla1_1, hla2_1): #print mismatch message only for valid alleles
            f.write(f"{input1_rows[i]['sample_name']} - {gene}: no match: {hla1_2} vs {hla2_2}\n")
        elif [HLA('X')] in (hla1_2, hla2_2):
            f.write(f"{input1_rows[i]['sample_name']} - {gene}: no match: {hla1_1} vs {hla2_1}\n")
        else: f.write(f"{input1_rows[i]['sample_name']} - {gene}: no match for both alleles: {hla1_1} and {hla1_2} vs {hla2_1} and {hla2_2}\n")
    elif score == 1: #one allele did not match, mismatch message depends on which pairs matched
        if matched_pairs[0] == 1: #the first pair in matched_pairs (if there even are 2) determines the mismatch message
            hla1 = hla1_2
            hla2 = hla2_2
        elif matched_pairs[0] == 2:
            hla1 = hla1_1
            hla2 = hla2_1
        elif matched_pairs[0] == 3:
            hla1 = hla1_2
            hla2 = hla2_1
        elif matched_pairs[0] == 4:
            hla1 = hla1_1
            hla2 = hla2_2
        if [HLA('X')] not in (hla1, hla2) and [HLA('empty')] not in (hla1, hla2): #print mismatch message only for valid alleles
            f.write(f"{input1_rows[i]['sample_name']} - {gene}: no match: {hla1} vs {hla2}\n")
    else: return #if score = 2, no mismatch message needs to be printed
    
def main(input1, input2, resolution_arg, method, genes, outdir):
    
    assert method in {'all', 'any'}, f'{method}: no valid option for --method argument: choose either any or all'
    if resolution_arg == 'None': resolution = None #support --resolution None
    else: resolution = resolution_arg

    """Create output file, parse hla genes and headers, read input files, match hla alleles, calculate allele score"""
    #create output txt file 
    output_file = '' #create txt file name
    for path in [input1, input2]:
        file = path.split('/')[-1] #get file name
        name = '.'.join(file.split('.')[0:-1]) #remove .csv
        output_file += f'{name}-'
    output_file += f'{resolution}-{method}-checked.txt'
    if outdir == sys.stdout:
        f = sys.stdout
    else: 
        if outdir[-1:] == '/': outdir = outdir[:-1] #remove / from end of outdir if present
        f = open(f'{outdir}/{output_file}', 'w')
    f.write(f"matching resolution used: {resolution}\nmatching method used: {method}\n")

    #parse genes that need to be checked
    hla_genes = []
    for gene in genes:
        hla_genes.append(f'HLA-{gene}')

    if f != sys.stdout: print(f'Genes that are being matched: {", ".join(hla_genes)}')
    f.write(f'Genes that are being matched: {", ".join(hla_genes)}\n')

    #read input files
    input_rows = []
    for file in [input1, input2]:
        open_file = open(file, newline='')
        reader_file = csv.DictReader(open_file)
        next(reader_file) #skip header
        input_rows.append(list(reader_file))
    input1_rows = input_rows[0]
    input2_rows = input_rows[1]
    #check if all genes are present in the input
    for gene in genes:
        assert input1_rows[0][f'HLA-{gene}'] != None, 'Not all genes that are being matched are present in the input files'
        assert input2_rows[0][f'HLA-{gene}'] != None, 'Not all genes that are being matched are present in the input files'

    #check both csv files have the same amount of samples
    assert len(input1_rows) == len(input2_rows), "csv files have different amount of samples"

    f.write(f'Input files: {input1.split("/")[-1]} vs {input2.split("/")[-1]}\n\n')

    #check if hla-types match and calculate percentage of correct alleles
    allele_score = 0 #counts correct alleles
    total_valid = 0  #counts total valid alleles
    total_inc_nomen = 0 #counts total alleles with incorrect nomenclature
    total_empty = 0 #counts total empty alleles
    for i in range(0,len(input1_rows)):
        for gene in hla_genes:
            hla1_1, hla1_2, hla2_1, hla2_2, alleles_validity = get_hla_class(i, gene, input1_rows, input2_rows)
            score, matched_pairs = match_pairs(hla1_1, hla1_2, hla2_1, hla2_2, resolution, method)
            allele_score += score
            total_valid += alleles_validity[0]
            total_empty += alleles_validity[1]
            mismatch_message(f, input1_rows, i, gene, score, matched_pairs, hla1_1, hla1_2, hla2_1, hla2_2)
    if total_valid != 0:
        perc_match = round(100*allele_score/total_valid, 2)
    else:
        f.write('No valid alleles recognized, cannot calculate percentage matched')
        perc_match = '-'
    if f != sys.stdout:
        print(f'Percentage of alleles that match: {str(perc_match)}% \nsee {outdir}/{output_file} for detailed result')
    f.write(f'\nNumber of alleles excluded due to an empty result: {total_empty}\n')
    f.write(f'Number of alleles included: {total_valid}\n')
    f.write(f'Number of included alleles that match: {allele_score}\n')
    f.write(f'Percentage of included alleles that match: {str(perc_match)}%\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input1", required=True, help="Input 1 CSV file to be matched")
    parser.add_argument("--input2", required=True, help="Input 2 CSV file to be matched")
    parser.add_argument("--resolution", default=None, help="Resolution at which matching should be done")
    parser.add_argument("--method", default='any', help = "Method for matching with multiple HLA options: any or all")
    parser.add_argument("--genes", nargs='+', default=['A','B','C','DRB1','DRB3','DRB4','DRB5','DQA1','DQB1','DPB1'], help="Genes to include")
    parser.add_argument("--outdir", default = sys.stdout, help = "Output directory for the matching result")

    args = parser.parse_args()

    main(args.input1, args.input2, args.resolution, args.method, args.genes, args.outdir)
