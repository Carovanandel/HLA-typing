[![Continuous Integration](https://github.com/Carovanandel/HLA-typing/actions/workflows/ci.yml/badge.svg)](https://github.com/Carovanandel/HLA-typing/actions/workflows/ci.yml)
[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pep.databio.org)
![GitHub release](https://img.shields.io/github/v/release/Carovanandel/HLA-typing)
![Commits since latest release](https://img.shields.io/github/commits-since/Carovanandel/HLA-typing/latest)

# HLA-typing
Snakemake file and python scripts for HLA-typing benchmark project

## Installation
Download the repository from github
```bash
git clone https://github.com/Carovanandel/HLA-typing.git
```

Install and activate the
[conda](https://docs.conda.io/en/latest/miniconda.html)
environment.
```bash
conda env create --file environment.yml
conda activate HLA-typing
```

Next, install singularity in the environment:
```bash
conda install singularity
export SINGULARITY_CACHEDIR=/exports/me-lcco-aml-hpc/cavanandel/.singularity
mkdir -p ${SINGULARITY_CACHEDIR}
```

The snakemake pipeline can then be executed with this environment using:
```bash
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --use-singularity --singularity-args ' --cleanenv --bind /tmp' --singularity-prefix '~/.singularity/cache/snakemake' --configfile tests/config.json --config pepfile=tests/pep/samples.csv --snakefile Snakefile --until T1K seq2hla optitype
```

## Installation for running the SpecHLA rule:
As SpecHLA currently does not have a container in BioContainers, the tool has to be installed in a separate environment.
Download the specHLA repository from github and create a conda environment 'spechla_env' using the environment-spechla.yml file in this repository
```bash
git clone https://github.com/deepomicslab/SpecHLA.git --depth 1
cd SpecHLA/
conda env create --prefix=./spechla_env -f ../HLA-Typing/environment-spechla.yml
conda activate ./spechla_env
```

Next, make the scripts in SpecHLA/bin/ executable and index the database
```bash
chmod +x -R bin/*
unset LD_LIBRARY_PATH && unset LIBRARY_PATH 
bash index.sh
```

The specHLA snakemake rule can then be executed with this environment active, using:
```bash
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --configfile tests/config.json--config pepfile=tests/pep/samples.csv --cores 1 --snakefile Snakefile --until spechla
```
## Installation for running the ArcasHLA rule
ArcasHLA does have a container in BioContainers, downloading the IMGT/HLA database during installation can give 
issues with the read-only file system of a container. Thus, ArcasHLA also needs to be installed in a separate 
environment. Create a conda environment using the environment-arcashla.yml file in this repository
```bash
conda env create -f ../HLA-Typing/environment-arcashla.yml
conda activate arcashla
```

Add the ArcasHLA bin folder to the system PATH variable, so the ArcasHLA commands are found
```bash
export PATH=~/miniforge3/envs/arcashla/bin:$PATH
```

Currently, a bug in ArcasHLA prevents you from using the latest IMGT/HLA database version. 
See [GitHub issue.](https://github.com/RabadanLab/arcasHLA/issues/133).
To install the most recent version of the IMGT/HLA database that will work, install Git Large File Storage (LFS) 
and download IMGT/HLA version 3.46.0
```bash
git lfs install
arcasHLA reference --version 3.46.0
```

The ArcasHLA snakemake rule can then be executed with this environment active, using:
```bash
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --configfile tests/config.json --config pepfile=tests/pep/samples.csv --cores 1 --snakefile Snakefile --until arcashla
```

## Use of scripts to process results

### formatting.py and formatting_lab.py
Use formatting.py and formatting_lab.py to parse the tool and lab outputs in a common format to be used by HLA_check.py.
formatting.py currently supports the formatting of ArcasHLA, OptiType, Seq2HLA, SpecHLA and T1K. 
The formatting of any future tools can be added to this script.

CSV format required for HLA_check.py:
```
Header: 'sample_name', 'HLA-A', 'HLA-A (2)', 'HLA-B', 'HLA-B (2)', etc
1 line per sample: 'sample1', 'HLA-A*01:02', 'HLA-A*03:04', 'HLA-B*03:02/HLA-B*03:03', 'HLA-B*05:01', etc
```

### HLA_check.py
Use HLA_check.py to compare the HLA types between two CSV files for given genes, resolution and matching method. 
Ensure that the two files include the same samples in the same order.

Arguments:
```
--input1: input CSV file 1 to be matched
--input2: input CSV file 2 to be matched
--resolution (optional): resolution at which matching should be done. Default = longest shared resolution
--method (optional): method for matching with multiple HLA options: 'any' or 'all' alleles must match. Default = any
--genes (optional): genes to include in the matching. Default = A, B, C, DRB1, DRB3, DRB4, DRB5, DQA1, DQB1, DPB1
--outdir (optional): output directory for the matching results. Default = print output in stdout
```

### HLA.py
HLA.py contains the HLA class used by the other scripts.

### split_resolutions_lab.py
When the available resolution of the HLA types in the lab output varies, use split_resolutions_lab.py 
to create lab output files with HLA types of more than 2 and more than 3 resolution fields, 
used by get_results.py to calculate accuracy at these resolutions.

### get_results.py
Use get_results.py to compare HLA types in all tool files to the lab file for each gene at each resolution (at 'any' method), 
by subprocessing HLA_check.py for each matching. This script creates a results.csv file containing all accuracy scores, 
and the number of alleles used for the calculation. 
This script supports ArcasHLA, OptiType, Seq2HLA, SpecHLA and T1K, other tools can be added.

### parse_benchmarks.py (written by Redmar van den Berg)
Use this parse_benchmarks.py to parse all benchmark stats from the Snakemake pipeline into combined tsv files for each benchmark stat.

### check_nomenclature
This script is currently out of use, but can be used to check the laboratory data for correct HLA nomenclature 
and to replace HLA alleles with incorrect nomenclature with 'X'. Support for 'X' alleles is currently removed from 
HLA_check.py but can be added back.

### 

## Settings
There are two ways configuration options are set, in decreasing order
of priority.
1. Key-values pairs passed to snakemake using `--config`
2. In the specified `--configfile`.

## Tests
You can run the tests that accompany this pipeline with the following commands

```bash
# Check if requirements are installed, run linting on the Snakefile and run tests for HLA.py and HLA_check.py
pytest --kwd --tag sanity

# Test the pipeline settings in dry-run mode
pytest --kwd --tag dry-run

# Test the performance of the pipeline by running on the test data. Currently only T1K and Seq2HLA can be tested this way.
pytest --kwd --tag integration
```
