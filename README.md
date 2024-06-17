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
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --use-singularity --singularity-args ' --cleanenv --bind /tmp' --singularity-prefix '~/.singularity/cache/snakemake' --configfile tests/config.json --config pepfile=tests/pep/100_samples.csv --snakefile Snakefile --until T1K seq2hla optitype
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
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --configfile tests/config.json --config pepfile=tests/pep/100_samples.csv --cores 1 --snakefile Snakefile --until spechla
```
## Installation for running the ArcasHLA rule
ArcasHLA does have a container in BioContainers, but the downloading of the IMGT/HLA database 
during installation can give issues with the read-only file system of a container. Thus, ArcasHLA also 
needs to be installed in a separate environment. Create a conda environment using the environment-arcashla.yml file in this repository
```bash
conda env create -f ../HLA-Typing/environment-arcashla.yml
conda activate arcashla
```

Add the ArcasHLA bin folder to the system PATH variable, so the ArcasHLA commands are found
```bash
export PATH=~/miniforge3/envs/arcashla/bin:$PATH
```

Currently, a bug in ArcasHLA prevents you from using the latest IMGT/HLA database version. Another bug prevents you from downloading older IMGT/HLA databases. See [pull request.](https://github.com/RabadanLab/arcasHLA/issues/133)
Workaround: replace the ```~/miniforge3/envs/snakemake-arcas-hla/share/arcas-hla-0.6.0-0/dat``` folder with the ```arcas-hla-0.6.0-0/dat``` folder from this repository, which contains version 3.55.0 of the IMGT/HLA database
```bash
mv arcas-hla-0.6.0-0/dat ~/miniforge3/envs/snakemake-arcas-hla/share/arcas-hla-0.6.0-0/dat
```

The ArcasHLA snakemake rule can then be executed with this environment active, using:
```bash
snakemake --printshellcmds --jobs 1 --latency-wait 5 --notemp --keep-incomplete --configfile tests/config.json --config pepfile=tests/pep/100_samples.csv --cores 1 --snakefile Snakefile --until arcashla
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
