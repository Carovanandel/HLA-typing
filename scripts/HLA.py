#!/usr/bin/env python3
import re

class HLA:
    #initiate hla class
    def __init__(self, gene, allele = None, protein = None):
        self.gene = gene
        self.allele = allele
        self.protein = protein

    #represent hla as string
    def __str__(self):
        s = f"HLA-{self.gene}"
        if self.allele is not None:
            s += f"*{self.allele}"

        if self.protein is not None:
            s += f":{self.protein}"

        return s

    #repr() calls str()
    def __repr__(self):
        return str(self)

    #define the == operator behavior for hla class objects
    def __eq__(self, other):
        return all((
            self.gene == other.gene,
            self.allele == other.allele,
            self.protein == other.protein,
        ))

    #create hla class object from string
    @classmethod
    def from_str(cls, hla):
        if hla == '0': 
            return hla  #return '0' back if no allele is called
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