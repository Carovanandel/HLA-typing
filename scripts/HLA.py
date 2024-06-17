#!/usr/bin/env python3
import re
from typing import List, Union, Optional

class HLA:
    #HLA class with variables for each HLA resolution field
    def __init__(
            self, 
            gene: Optional[str],
            allele: Optional[str] = None,
            protein: Optional[str] = None,
            synonymous:Optional[str] = None,
            noncoding: Optional[str]=None,
            suffix: Optional[str] = None) -> None:
        self.gene = gene
        self.allele = allele
        self.protein = protein
        self.synonymous = synonymous
        self.noncoding = noncoding
        self.suffix = suffix

    #represent HLA as string
    def __str__(self) -> str:
        if self.gene is None:
            return '0'  #return 0 for empty HLA class
        s = f"HLA-{self.gene}"
        if self.allele is not None:
            s += f"*{self.allele}"

        if self.protein is not None:
            s += f":{self.protein}"

        if self.synonymous is not None:
            s += f":{self.synonymous}"
        if self.noncoding is not None:
            s += f":{self.noncoding}"
        if self.suffix is not None:
            s += self.suffix
        return s
        
    def __repr__(self) -> str:
        return str(self)

    #define the == operator behavior for hla class objects
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HLA):
            msg = f"Unsupported comparison between HLA and {type(other)}"
            raise NotImplementedError(msg)
        return all((
            self.gene == other.gene,
            self.allele == other.allele,
            self.protein == other.protein,
            self.synonymous == other.synonymous,
            self.noncoding == other.noncoding,
            self.suffix == other.suffix
        ))

    #create HLA class object from string
    @classmethod
    def from_str(cls, hla: str) -> "HLA":
        #nomenclature example: HLA-DRB1*13:01:01:02Q
        pattern = r"^HLA-(\w+)(\*\d+)?(:\d+)?(:\d+)?(:\d+)?([LSCAQN])?$"
        m = re.match(pattern, hla)

        if not m:
            raise ValueError(f"Invalid HLA description: {hla}")

        gene = m.group(1)
        allele = m.group(2)
        protein = m.group(3)
        synonymous = m.group(4)
        noncoding = m.group(5)
        suffix = m.group(6)

        #cut off the *
        allele = allele[1:] if allele else None
        #cut off the colons
        protein = protein[1:] if protein else None
        synonymous = synonymous[1:] if synonymous else None
        noncoding = noncoding[1:] if noncoding else None

        return HLA(gene, allele, protein, synonymous, noncoding, suffix)

    #return a list of the HLA resolution fields
    def fields(self) -> List[Union[str, None]]:
        return [
            self.gene,
            self.allele,
            self.protein,
            self.synonymous,
            self.noncoding,
            self.suffix
        ]

    #return a list of the HLA fields from a string
    @classmethod
    def fields_from_str(cls, hla: str) -> List[Union[str, None]]:
        hla_class = HLA.from_str(hla)
        return hla_class.fields()
    
    #test if two HLA types match at a given resolution
    def match(self, other: "HLA", resolution: Union[int, None] = None) -> bool:
        self_fields: List[Optional[str]]
        other_fields: List[Optional[str]]
        if resolution is None:
            self_fields = [x for x in self.fields() if x is not None]
            other_fields = [x for x in other.fields() if x is not None]
        else:
            r = int(resolution) + 1
            self_fields = self.fields()[:r]
            other_fields = other.fields()[:r]
        zipped = zip(self_fields, other_fields)
        for pair in zipped:
            if pair[0] != pair[1]:
                return False
        return True
