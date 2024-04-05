#!/usr/bin/env python3
import re

class HLA:
    def __init__(self, gene, allele = None, protein = None):
        self.gene = gene
        self.allele = allele
        self.protein = protein

    def __str__(self):
        s = f"HLA-{self.gene}"
        if self.allele is not None:
            s += f"*{self.allele}"

        if self.protein is not None:
            s += f":{self.protein}"

        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return all((
            self.gene == other.gene,
            self.allele == other.allele,
            self.protein == other.protein,
        ))

    @classmethod
    def from_str(cls, hla):
        assert hla.startswith("HLA-"), "Please use full HLA nomenclature"
        pattern = "HLA-(\\w+)(\\*\\d+)?(:\\d+)?"
        m = re.match(pattern, hla)
        gene = m.group(1)
        allele = m.group(2)
        protein = m.group(3)

        # Remember to cut off the *
        allele = allele[1:] if allele else None
        # Remember to cut off the colon
        protein = protein[1:] if protein else None

        return HLA(gene, allele, protein)
