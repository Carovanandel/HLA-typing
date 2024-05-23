#!/usr/bin/env python3
import argparse
from typing import Any, Dict, List, Generator
from collections import defaultdict
from statistics import mean

expected = [
    "s",
    "max_rss",
    "max_vms",
    "max_uss",
    "max_pss",
    "io_in",
    "io_out",
    "mean_load",
    "cpu_time",
]

def remove_human_readable(records: List) -> None:
    """The second fields holds time in h:m:s format"""
    del records[1]

def parse_benchmark_file(fname: str) -> Generator[Dict[str, float], Any, Any]:
    """Return records from a benchmark file"""
    with open(fname) as fin:
        header = next(fin).strip("\n").split("\t")
        remove_human_readable(header)
        assert header == expected
        for line in fin:
            spline = line.strip('\n').split('\t')
            remove_human_readable(spline)
            # Convert '-' to '0'. '-' happens when the analysis is too fast to
            # measure, which can happen during testing
            spline = ['0' if x == '-' else x for x in spline]
            yield {key: float(value) for key, value in zip(header, spline)}

def average_benchmark(fname: str) -> Dict[str, float]:
    """Return the average for each column in a benchmark file"""
    data = defaultdict(list)
    for record in parse_benchmark_file(fname):
        for key,value in record.items():
            data[key].append(value)

    return {key: mean(values) for key, values in data.items()}

def main(args):
    header = ["sample"] + args.tools
    print(*header, sep='\t')
    for sample in args.samples:
        # Initialise the dict with the current sample
        results = {"sample": sample }
        for tool in args.tools:
            # Make the file path
            fname = f"benchmarks/{tool}_{sample}.tsv"
            avg = average_benchmark(fname)
            results[tool] = avg[args.column]
        print(*(results[field] for field in header), sep='\t')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--column', help='Column from the benchmark')
    parser.add_argument('--samples', nargs='+')
    parser.add_argument('--tools', nargs='+')

    args = parser.parse_args()
    main(args)
