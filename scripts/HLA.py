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
        if self.gene == None:
            return '0'  #return 0 for empty HLA class
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
            return HLA(None) # return empty HLA class for 0 allele
        if '/' in hla:  #return list for multiple options (in lab result, tool results must only give top option)
            hla_options = hla.split('/')
            hla_list = []
            for option in hla_options:
                assert option.startswith("HLA-"), "Please use full HLA nomenclature"
                pattern = "HLA-(\\w+)(\\*\\d+)?(:\\d+)?"
                m = re.match(pattern, option)
                gene = m.group(1)
                allele = m.group(2)
                protein = m.group(3)
                 # Remember to cut off the *
                allele = allele[1:] if allele else None
                # Remember to cut off the colon
                protein = protein[1:] if protein else None
                hla_list.append(HLA(gene, allele, protein))
            return hla_list
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
    
    #testing if two hla-types match
    #method == 1 --> HLA-types must be identical
    #method == 2 --> If hla1 does not have a protein field, hla2 is allowed to have anything in the protein field
    def match(self, other, method):
        assert method == 1 or method == 2, 'method has to be 1 (identical) or 2 (resolution ambiguity allowed)'
        if method == 1: #HLA-types must be identical
            if self == other: return True
            else: return False
        if method == 2: #only if hla1 has a protein field, hla2 has to match
            if self.gene != other.gene or self.allele != other.allele:
                return False
            if self.protein != None and other.protein != None and self.protein != other.protein:
                return False
            else: return True
    