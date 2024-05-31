import subprocess
import csv

def run_hla_check(tool, lab, gene, resolution):
    """Run HLA_check.py and return result values"""
    command = ['python', '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/scripts/HLA_check.py', 
               '--input1', f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/{lab}.csv', 
               '--input2', f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/{tool}-output.csv', 
               '--genes', gene,
               '--resolution', str(resolution)]
    
    hla_check = subprocess.run(command, capture_output=True, text=True)

    if hla_check.returncode == 0:
        #print(hlacheck.stdout)
        stdout_lines = hla_check.stdout.split('\n')
        for line in stdout_lines:
            if line.startswith('Number of alleles excluded due to an empty result:'):
                total_empty = int(line.split(':')[-1])
            elif line.startswith('Number of alleles included:'):
                total_valid = int(line.split(':')[-1])
            elif line.startswith('Number of included alleles that match:'):
                num_match = int(line.split(':')[-1])
            elif line.startswith('Percentage of included alleles that match:'):
                perc_match = line.split(':')[-1].strip('%')
                if perc_match == ' -': perc_match = '-'
                else: perc_match = float(perc_match)
        return total_empty, total_valid, num_match, perc_match
    else:
        print(f"{tool} - {gene} - {resolution}: HLA_check.py execution failed with error: {hla_check.stderr}")
        return None, None, None, None

#create result.csv file
results_header = ['Tool', 'Gene', 'Resolution', 'Method', 'Total empty', 'Total valid', 'Number matched', 'Percentage matched']
results_file = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/results.csv'
open_results = open(results_file, 'w', newline = '')
results_writer = csv.DictWriter(open_results, delimiter=',', fieldnames=results_header)
results_writer.writeheader()

#lab hla-type.csv and genes and resolutions supported by each tool
t1k = {'tool': 't1k',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DRB3', 'DRB4', 'DRB5', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2, 3]}

seq2hla = {'tool': 'seq2hla',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2]}

optitype = {'tool': 'optitype',
       'genes' : ['A', 'B', 'C'],
       'resolutions' : ['None', 1, 2]}

spechla = {'tool': 'spechla',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2, 3]}

arcashla = {'tool': 'arcashla',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DRB3', 'DRB5', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2, 3]}

two_fields_split = [('1-field-hla-type', 1), ('2-fields-hla-type', 2), ('3-fields-hla-type', 2)]
three_fields_split = [('1-field-hla-type', 1), ('2-fields-hla-type', 2), ('3-fields-hla-type', 3)]

def match_fields(resolution, results):
    """function to report the amount of alleles matched at each resolution, in the sum for resolution 2 and 3"""
    one_match = results[0][2]
    one_checked = results[0][1]
    if resolution == 2:
        two_match= results[1][2] + results[2][2]
        two_checked = results[1][1]+results[2][1]
        three_match = None
        three_checked = None
    else:
        two_match = results[1][2]
        two_checked = results[1][1]
        three_match = results[2][2]
        three_checked = results[2][1]

    return one_match, two_match, three_match, one_checked, two_checked, three_checked

#run HLA_check for each tool/gene/resolution combination and write to results.csv
for tool in [t1k, seq2hla, optitype, spechla, arcashla]:
    for gene in tool['genes']:
        for resolution in tool['resolutions']:
            results_row = {column: '' for column in results_header}
            results_row.update({'Tool': tool['tool'], 'Gene': gene, 'Resolution': resolution, 'Method': 'any'})
            if resolution in ['None', 1]:
                total_empty, total_valid, num_match, perc_match = run_hla_check(tool['tool'], 'full-hla-type', gene, resolution)
            elif resolution in [2, 3]:
                total_empty, total_valid, num_match, perc_match = run_hla_check(tool['tool'], f'{resolution}-fields-hla-type', gene, resolution)
            results_row.update({'Total empty': total_empty,
                                'Total valid': total_valid,
                                'Number matched': num_match,
                                'Percentage matched': perc_match})
            results_writer.writerow(results_row)