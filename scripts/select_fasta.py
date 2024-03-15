#!/usr/bin/env python3

import argparse
import sys
from dataclasses import dataclass

@dataclass
class Fasta:
    header: str
    sequence: str

    def __str__(self):
        return f">{self.header}\n{self.sequence}"

    @property
    def name(self):
        return self.header.split(' ')[0]

def parse_fasta(fname):
    """Read the fasta file into Fasta objects"""
    with open(fname) as fin:
        # Set up
        line = next(fin)
        assert line.startswith(">")
        header = line[1:-1]
        seq = ""
        for line in fin:
            if line.startswith(">"):
                yield Fasta(header, seq)
                header = line[1:-1]
                seq =""
            else:
                seq += line.strip('\n')
        yield Fasta(header, seq)


def main(fname, names):
    for record in parse_fasta(fname):
        if record.name in names:
            print(record)
            names.remove(record.name)

    for not_found in names:
        print(f"Not found: {not_found}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fasta", help="Fasta file to select entries from")
    parser.add_argument("--names", nargs='+', required=True, help="Entry names to output")

    args =parser.parse_args()

    main(args.fasta, args.names)
