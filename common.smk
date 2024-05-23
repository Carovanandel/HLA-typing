containers = {
    "T1K": "docker://quay.io/biocontainers/t1k:1.0.5--h43eeafb_0",
    "seq2hla": "docker://quay.io/biocontainers/seq2hla:2.3--hdfd78af_1",
    "optitype": "docker://quay.io/biocontainers/optitype:1.3.5--hdfd78af_2",
    "dnaio": "docker://quay.io/biocontainers/mulled-v2-2996a7d035117c4238b2b801e740a69df21d91e1:6b3ae5f1a97f370227e8134ba3efc0e318b288c3-0",
}

default = dict()
default["repeat"] = 1

# Apply the options specified to snakemake, overwriting the default settings
default.update(config)

# Set the updated dict as the configuration for the pipeline
config = default


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
