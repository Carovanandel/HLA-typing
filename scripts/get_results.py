import subprocess
import csv

def run_hla_check(tool, lab, gene, resolution):
    """Run HLA_check.py and return result values"""
    command = ['python', 'HLA_check.py', 
               '--input1', f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/{lab}.csv', 
               '--input2', f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/{tool}-output.csv', 
               '--genes', gene,
               '--resolution', str(resolution)]
    
    hla_check = subprocess.run(command, capture_output=True, text=True)

    if hla_check.returncode == 0:
        #print(hlacheck.stdout)
        stdout_lines = hla_check.stdout.split('\n')
        for line in stdout_lines:
            if line.startswith('Number of alleles excluded due to incorrect nomenclature:'):
                total_inc_nomen = int(line.split(':')[-1])
            elif line.startswith('Number of alleles excluded due to an empty result:'):
                total_empty = int(line.split(':')[-1])
            elif line.startswith('Number of alleles included:'):
                total_valid = int(line.split(':')[-1])
            elif line.startswith('Number of included alleles that match:'):
                num_match = int(line.split(':')[-1])
            elif line.startswith('Percentage of included alleles that match:'):
                perc_match = line.split(':')[-1].strip('%')
                if perc_match == ' -': perc_match = '-'
                else: perc_match = float(perc_match)
        return total_inc_nomen, total_empty, total_valid, num_match, perc_match
    else:
        print(f"{tool} - {gene} - {resolution}: HLA_check.py execution failed with error: {hla_check.stderr}")
        return None, None, None, None, None

#create result.csv file
results_header = ['Tool', 'Gene', 'Resolution', 'Method', 'Total inc nomen', 'Total empty', 'Total valid', 'Number matched', 'Percentage matched']
results_file = '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/results.csv'
open_results = open(results_file, 'w', newline = '')
results_writer = csv.DictWriter(open_results, delimiter=',', fieldnames=results_header)
results_writer.writeheader()

#lab hla-type.csv and genes and resolutions supported by each tool
t1k = {'tool': 't1k',
       'lab': 'correct-nomen-hla-type',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DRB3', 'DRB4', 'DRB5', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2, 3]}

seq2hla = {'tool': 'seq2hla',
       'lab': 'correct-nomen-hla-type',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2]}

optitype = {'tool': 'optitype',
       'lab': 'correct-nomen-hla-type',
       'genes' : ['A', 'B', 'C'],
       'resolutions' : ['None', 1, 2, 3]}

spechla = {'tool': 'spechla',
       'lab': 'small-correct-nomen-hla-type',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2, 3]}

arcashla = {'tool': 'arcashla',
       'lab': 'small-correct-nomen-hla-type',
       'genes' : ['A', 'B', 'C', 'DRB1', 'DRB3', 'DRB4', 'DRB5', 'DQA1', 'DQB1', 'DPB1'],
       'resolutions' : ['None', 1, 2, 3]}

#run HLA_check for each tool/gene/resolution combination and write to results.csv
for tool in [t1k, seq2hla, optitype, spechla, arcashla]:
    for gene in tool['genes']:
        for resolution in tool['resolutions']:
            results_row = {column: '' for column in results_header}
            results_row.update({'Tool': tool['tool'], 'Gene': gene, 'Resolution': resolution, 'Method': 'any'})
            total_inc_nomen, total_empty, total_valid, num_match, perc_match = run_hla_check(tool['tool'], tool['lab'], gene, resolution)
            results_row.update({'Total inc nomen': total_inc_nomen,
                                'Total empty': total_empty,
                                'Total valid': total_valid,
                                'Number matched': num_match,
                                'Percentage matched':perc_match})
            results_writer.writerow(results_row)