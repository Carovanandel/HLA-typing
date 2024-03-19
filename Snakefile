include: "common.smk"


pepfile: config["pepfile"]


rule all:
    input:
        T1K=expand(
            "output/{sample}/T1K/{sample}_allele.tsv",
            sample=pep.sample_table["sample_name"],
        ),
        seq2hla=expand(
            "output/{sample}/seq2hla/{sample}-ClassI-class.HLAgenotype4digits",
            sample=pep.sample_table["sample_name"],
        ),
        arcashla=expand(
            "output/{sample}/arcashla/{sample}.genotype.json",
            sample=pep.sample_table["sample_name"],
        ),


rule T1K:
    input:
        f=get_forward,
        r=get_reverse,
        reference=config["T1K_fasta"],
    output:
        allele="output/{sample}/T1K/sample1_allele.tsv",
        genotype="output/{sample}/T1K/sample1_genotype.tsv",
    log:
        "output/log/{sample}.T1K.txt",
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
        classI_4digits="output/{sample}/seq2hla/{sample}-ClassI-class.HLAgenotype4digits",
        ambiguity="output/{sample}/seq2hla/{sample}.ambiguity",
    log:
        "output/log/{sample}.seq2hla.txt",
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


rule arcashla:
    input:
        f=get_forward,
        r=get_reverse,
    output:
        genotype="output/{sample}/arcashla/{sample}.genotype.json",
    log:
        "output/log/{sample}.arcashla.txt",
    container:
        containers["arcashla"]
    threads: 1
    shell:
        """
        arcasHLA genotype \
        {input.f} \
        {input.r} \
        --genes A,B,C \
        --outdir $(dirname {output.genotype})/{wildcards.sample} \
        --threads {threads} \
        --verbose \
        --log {log}
        """
