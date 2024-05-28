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
        optitype=expand(
            "output/{sample}/optitype/{sample}.tsv",
            sample=pep.sample_table["sample_name"],
        ),
        spechla=expand(
            "output/{sample}/spechla/hla.result.txt",
            sample=pep.sample_table["sample_name"],
        ),
        arcashla=expand(
            "output/{sample}/arcashla/{sample}.genotype.json",
            sample=pep.sample_table["sample_name"],
        ),
        gather_benchmarks="benchmarks/s.tsv",


rule T1K:
    input:
        f=get_forward,
        r=get_reverse,
        reference=config["T1K_fasta"],
    output:
        allele="output/{sample}/T1K/{sample}_allele.tsv",
        genotype="output/{sample}/T1K/{sample}_genotype.tsv",
    log:
        "output/log/{sample}.T1K.txt",
    benchmark:
        repeat("benchmarks/T1K_{sample}.tsv", config["repeat"])
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
    benchmark:
        repeat("benchmarks/seq2hla_{sample}.tsv", config["repeat"])
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


rule optitype:
    input:
        f=get_forward,
        r=get_reverse,
    output:
        genotype="output/{sample}/optitype/{sample}.tsv",
    log:
        "output/log/{sample}.optitype.txt",
    benchmark:
        repeat("benchmarks/optitype_{sample}.tsv", config["repeat"])
    container:
        containers["optitype"]
    threads: 1
    shell:
        """
        OptiTypePipeline.py \
        --input {input.f} {input.r} \
        --rna \
        --outdir $(dirname {output.genotype}) \
        --verbose 2> {log}
        mv output/{wildcards.sample}/optitype/*/*result.tsv {output.genotype}
        """


rule spechla:
    input:
        f=get_forward,
        r=get_reverse,
    output:
        result="output/{sample}/spechla/hla.result.txt",
    log:
        "output/log/{sample}.spechla.txt",
    benchmark:
        repeat("benchmarks/spechla_{sample}.tsv", config["repeat"])
    threads: 1
    params:
        spechla_path=config["spechla_path"],
    shell:
        """
        bash {params.spechla_path}/script/whole/SpecHLA.sh \
        -u 1 \
        -j {threads} \
        -n {wildcards.sample} \
        -1 {input.f} \
        -2 {input.r} \
        -o $(dirname {output.result}) \
        2> {log} 
        mv output/{wildcards.sample}/spechla/{wildcards.sample}/hla.result.txt {output.result}
        """


rule arcashla:
    input:
        f=get_forward,
        r=get_reverse,
    output:
        genotype="output/{sample}/arcashla/{sample}.genotype.json",
    log:
        "output/log/{sample}.arcashla.txt",
    benchmark:
        repeat("benchmarks/arcashla_{sample}.tsv", config["repeat"])
    threads: 1
    shell:
        """
        arcasHLA genotype \
        {input.f} \
        {input.r} \
        --genes A,B,C,DRB1,DRB3,DRB5,DQA1,DQB1,DPB1 \
        --outdir $(dirname {output.genotype}) \
        --threads {threads} \
        --verbose \
        --log {log}
        """


rule gather_benchmarks:
    input:
        T1K=expand(
            "benchmarks/T1K_{sample}.tsv", sample=pep.sample_table["sample_name"]
        ),
        seq2hla=expand(
            "benchmarks/seq2hla_{sample}.tsv", sample=pep.sample_table["sample_name"]
        ),
        optitype=expand(
            "benchmarks/optitype_{sample}.tsv", sample=pep.sample_table["sample_name"]
        ),
        spechla=expand(
            "benchmarks/spechla_{sample}.tsv", sample=pep.sample_table["sample_name"]
        ),
        arcashla=expand(
            "benchmarks/arcashla_{sample}.tsv", sample=pep.sample_table["sample_name"]
        ),
        script=srcdir("scripts/parse-benchmark.py"),
    params:
        samples=list(pep.sample_table["sample_name"]),
    output:
        seconds="benchmarks/s.tsv",
        cpu_time="benchmarks/cpu_time.tsv",
        max_rss="benchmarks/max_rss.tsv",
    log:
        "log/gather_benchmarks.txt",
    container:
        containers["dnaio"]
    shell:
        """
        for column in s cpu_time max_rss; do
          python3 {input.script} \
              --samples {params.samples} \
              --tools T1K seq2hla optitype spechla arcashla \
              --column ${{column}} > benchmarks/${{column}}.tsv 2>> {log}
        done
        """
