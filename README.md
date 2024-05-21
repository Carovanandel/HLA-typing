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
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --use-singularity --singularity-args ' --cleanenv --bind /tmp' --singularity-prefix '~/.singularity/cache/snakemake' --configfile tests/config.json --config pepfile=tests/pep/100_samples.csv --snakefile Snakefile
```

## Installation for running the specHLA rule:
Download the specHLA repository from github and create the environment 'spechla_env' using the environment-spechla.yml file in this (HLA-typing) repository
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
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --configfile tests/config.json --config pepfile=tests/pep/100_samples.csv --cores 1 --snakefile Snakefile --until spechla
```

## Settings
There are two ways configuration options are set, in decreasing order
of priority.
1. Key-values pairs passed to snakemake using `--config`
2. In the specified `--configfile`.

## Tests
You can run the tests that accompany this pipeline with the following commands

```bash
# Check if requirements are installed, and run linting on the Snakefile
pytest --kwd --tag sanity

# Test the pipeline settings in dry-run mode
pytest --kwd --tag dry-run

# Test the performance of the pipeline by running on the test data
pytest --kwd --tag integration
```
