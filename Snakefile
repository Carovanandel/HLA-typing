include: "common.smk"


pepfile: config["pepfile"]


rule all:
    input:
        T1K=expand(
            "{sample}/T1K/{sample}_allele.tsv", sample=pep.sample_table["sample_name"]
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
