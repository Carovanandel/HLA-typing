import pytest
import sys
import os
#get the directory path with the HLA.py and HLA_check script to import functions
hla_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')) 
sys.path.insert(0, hla_dir)
from HLA import HLA

#bypass sys.argv assertion error in HLA_check.py
sys.argv = ['HLA_check.py','scripts/test_files/testoutput_lab.csv', 
            'scripts/test_files/testoutput_tool.csv', '2', 'all']
from HLA_check import get_hla_list, check_match, match_pairs

#test creating a list with all hla options from a string
hla_list = [
    ('HLA-A*01:01', ([HLA('A','01','01')], 'valid')),
    ('HLA-A*01:01/HLA-A*01:02', ([HLA('A','01','01'),HLA('A','01','02')], 'valid')),
    ('HLA-B*01:01/HLA-B*01', ([HLA('B','01'), HLA('B','01','01')], 'valid')),
    ('HLA-C*01:01N', ([HLA('C','01','01',None,None,'N')], 'valid')),
    ('', ([HLA('empty')], 'empty')),
    #('X', ([HLA('X')], 'inc_nomen')) #support for 'X' incorrect nomenclature has been removed from HLA_check, can be added back
]

@pytest.mark.parametrize("hla, expected", hla_list)
def test_get_hla_list(hla, expected):
    assert get_hla_list(hla) == expected

#test match function comparing two hla alleles at a given resolution and all/any matching method
match = [
    (["HLA-A"], ["HLA-A"], None, 'all', True),
    (["HLA-A"], ["HLA-A"], None, 'any', True),
    (["HLA-A", "HLA-a"], ["HLA-A"], None, 'all', False),
    (["HLA-A", "HLA-a"], ["HLA-A"], None, 'any', True),
    (["HLA-A", "HLA-a"], ["HLA-A", "HLA-a"], None, 'all', True),
    ([], [], None, 'any', False),
]

@pytest.mark.parametrize('hla1, hla2, resolution, method, expected', match)
def test_match(hla1, hla2, resolution, method, expected):
    HLA1 = [HLA.from_str(x) for x in hla1]
    HLA2 = [HLA.from_str(x) for x in hla2]
    assert check_match(HLA1, HLA2, resolution, method) == expected
    assert check_match(HLA2, HLA1, resolution, method) == expected

#test match_pairs function comparing two sets of two hla alleles
pairs = [
    (
        ["HLA-A", "HLA-B"],
        ["HLA-C"],
        ["HLA-A", "HLA-C"],
        ["HLA-A", "HLA-B"],
        None, 'any', (2, [1, 3, 4])
    ),
    (
        ["HLA-A", "HLA-B"],
        ["HLA-C"],
        ["HLA-A"],
        ["HLA-A", "HLA-B"],
        None, 'any', (1, [1, 3])
    ),
    (
        ["HLA-A"],
        ["HLA-C"],
        ["HLA-B"],
        ["HLA-D"],
        None, 'any', (0, [])),
]

@pytest.mark.parametrize('hla1_1, hla1_2, hla2_1, hla2_2, resolution, method, expected', pairs)
def test_match_pairs(hla1_1, hla1_2, hla2_1, hla2_2, resolution, method, expected):
    # Convert the string representation to HLA
    HLA1_1 = [HLA.from_str(x) for x in hla1_1]
    HLA1_2 = [HLA.from_str(x) for x in hla1_2]
    HLA2_1 = [HLA.from_str(x) for x in hla2_1]
    HLA2_2 = [HLA.from_str(x) for x in hla2_2]
    assert match_pairs(HLA1_1, HLA1_2, HLA2_1, HLA2_2, resolution, method) == expected
