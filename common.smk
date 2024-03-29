containers = {
    "T1K": "docker://quay.io/biocontainers/t1k:1.0.5--h43eeafb_0",
    "seq2hla": "docker://quay.io/biocontainers/seq2hla:2.3--hdfd78af_1",
    "arcashla": "docker://quay.io/biocontainers/arcas-hla:0.6.0--hdfd78af_0",
    "optitype": "docker://quay.io/biocontainers/optitype:1.3.5--hdfd78af_2",
}


def get_outfile():
    return "outputfile.txt"


def get_forward(wildcards):
    forward = pep.sample_table.loc[wildcards.sample, "forward"]

    # If a single fastq file is specified, forward will be a string
    if isinstance(forward, str):
        return [forward]
    # If multiple fastq files were specified, forward will be a list
    else:
        return forward


def get_reverse(wildcards):
    reverse = pep.sample_table.loc[wildcards.sample, "reverse"]

    # If a single fastq file is specified, reverse will be a string
    if isinstance(reverse, str):
        return [reverse]
    # If multiple fastq files were specified, reverse will be a list
    else:
        return reverse
