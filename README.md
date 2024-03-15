[![Continuous Integration](https://github.com/Carovanandel/HLA-typing/actions/workflows/ci.yml/badge.svg)](https://github.com/Carovanandel/HLA-typing/actions/workflows/ci.yml)
[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pep.databio.org)
![GitHub release](https://img.shields.io/github/v/release/Carovanandel/HLA-typing)
![Commits since latest release](https://img.shields.io/github/commits-since/Carovanandel/HLA-typing/latest)

# HLA-typing
Example of a snakemake project

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

## Settings
There are two ways configuration options are set, in decreasing order
of priority.
1. Key-values pairs passed to snakemake using `--config`
2. In the specified `--configfile`.

### Supported settings
The following settings are available for the pipeline.
| Option               | Type                  | Explanation                             |
| ---------------------| -----------------     | --------------------------------------- |
| setting1             | Required string       | The first setting                       |
| setting2             | Required settingsfile | A file with some settings               |
| setting3             | Required string       | A third setting                         |

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
