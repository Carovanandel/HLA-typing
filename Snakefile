include: "common.smk"


pepfile: config["pepfile"]


rule all:
    input:
        T1K=expand(
            "{sample}/T1K/{sample}_allele.tsv", sample=pep.sample_table["sample_name"]
        ),
        seq2HLA=expand(
            "{sample}/seq2hla/{sample}-ClassI-class.HLAgenotype4digits", sample=pep.sample_table["sample_name"]
        ),


rule T1K:
    input:
        f=get_forward,
        r=get_reverse,
        reference=config["T1K_fasta"],
    output:
        allele="{sample}/T1K/sample1_allele.tsv",
        genotype="{sample}/T1K/sample1_genotype.tsv",
    log:
        "log/{sample}.T1K.txt",
    container:
        containers["T1K"]
    threads: 1
    shell:
        """
        run-t1k \
            -1 {input.f} \
            -2 {input.r} \
            -o {wildcards.sample} \
            --od $(dirname {output.allele}) \
            -t {threads} \
            --preset hla \
            -f {input.reference} 2> {log}
        """

rule seq2hla:
    input:
        f=get_forward,
        r=get_reverse,
    output:
        classI_4digits="{sample}/seq2hla/{sample}-ClassI-class.HLAgenotype4digits", 
        ambiguity="{sample}/seq2hla/{sample}.ambiguity",
    log:
        "log/{sample}.seq2hla.txt",
    container:
        containers["seq2hla"]
    threads: 1
    shell:
        """
        seq2HLA \
        -1 {input.f} \
        -2 {input.r} \
        -r $(dirname {output.classI_4digits})/{wildcards.sample} 2> {log}
        """
