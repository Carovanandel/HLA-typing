import subprocess
import csv

### Use this script to compare HLA types in all tool files to the lab file for each gene at each resolution (at 'any' method)
### This script supports ArcasHLA, OptiType, Seq2HLA, SpecHLA and T1K. Other tools can be added

def run_hla_check(tool, lab, gene, resolution):
    """Run HLA_check.py and return result values"""
    command = ['python', '/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/scripts/HLA_check.py', 
               '--input1', f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/lab/{lab}.csv', 
               '--input2', f'/exports/me-lcco-aml-hpc/cavanandel/HLA-typing/output-formatted/{tool}-output.csv', 
               '--genes', gene,
               '--resolution', str(resolution)]
    
    hla_check = subprocess.run(command, capture_output=True, text=True)

    if hla_check.returncode == 0:
        #print(hlacheck.stdout) #for debugging
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

#genes and resolutions supported by each tool
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

#run HLA_check for each tool/gene/resolution combination and write to results.csv
for tool in [t1k, seq2hla, optitype, spechla, arcashla]:
    for gene in tool['genes']:
        for resolution in tool['resolutions']:
            results_row = {column: '' for column in results_header}
            results_row.update({'Tool': tool['tool'], 'Gene': gene, 'Resolution': resolution, 'Method': 'any'})
            if resolution in ['None', 1]: #full hla-type files are used for comparison at shortest and 1-field resolution
                total_empty, total_valid, num_match, perc_match = run_hla_check(tool['tool'], 'full-hla-type', gene, resolution)
            elif resolution in [2, 3]: #filtered 2+ and 3+ fields files are used for comparison at these resolutions
                total_empty, total_valid, num_match, perc_match = run_hla_check(tool['tool'], f'{resolution}-fields-hla-type', gene, resolution)
            results_row.update({'Total empty': total_empty,
                                'Total valid': total_valid,
                                'Number matched': num_match,
                                'Percentage matched': perc_match})
            results_writer.writerow(results_row)