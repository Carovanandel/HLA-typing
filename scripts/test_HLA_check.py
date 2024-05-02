import pytest
import sys
from HLA import HLA

#bypass sys.argv assertion error in HLA_check.py
sys.argv = ['HLA_check.py','scripts/test_files/testoutput_lab.csv', 
            'scripts/test_files/testoutput_tool.csv', '2', 'all']
from HLA_check import get_hla_list, check_match, match_pairs

hla_list = [
    ('HLA-A*01:01', [HLA('A','01','01')]),
    ('HLA-A*01:01/HLA-A*01:02', [HLA('A','01','01'),HLA('A','01','02')]),
    ('HLA-B*01:01/HLA-B*01', [HLA('B','01'), HLA('B','01','01')]),
    ('HLA-C*01:01N', [HLA('C','01','01',None,None,'N')]),
    ('', []),
]

@pytest.mark.parametrize("hla, expected", hla_list)
def test_get_hla_list(hla, expected):
    assert get_hla_list(hla) == expected

match = [
    (["HLA-A"], ["HLA-A"], None, 'all', True),
    (["HLA-A"], ["HLA-A"], None, 'any', True),
    (["HLA-A", "HLA-a"], ["HLA-A"], None, 'all', False),
    (["HLA-A", "HLA-a"], ["HLA-A"], None, 'any', True),
    (["HLA-A", "HLA-a"], ["HLA-A", "HLA-a"], None, 'all', True),
    ([], [], None, 'any', True),
    ([], [], None, 'all', True),
    ([], [], 2, 'any', True),
    ([], [], 2, 'all', True),
]

@pytest.mark.parametrize('hla1, hla2, resolution, method, expected', match)
def test_match(hla1, hla2, resolution, method, expected):
    HLA1 = [HLA.from_str(x) for x in hla1]
    HLA2 = [HLA.from_str(x) for x in hla2]
    assert check_match(HLA1, HLA2, resolution, method) == expected
    assert check_match(HLA2, HLA1, resolution, method) == expected

pairs = [
    ([HLA('A'),HLA('B')], [HLA('C')], [HLA('A'), HLA('C')], [HLA('A'), HLA('B')], None, 'any', (2, [1, 3, 4])),
    ([HLA('A'),HLA('B')], [HLA('C')], [HLA('A')], [HLA('A'), HLA('B')], None, 'any', (1, [1, 3])),
    ([HLA('A')], [HLA('C')], [HLA('B')], [HLA('D')], None, 'any', (0, [])),
]

@pytest.mark.parametrize('hla1_1, hla1_2, hla2_1, hla2_2, resolution, method, expected', pairs)
def test_match_pairs(hla1_1, hla1_2, hla2_1, hla2_2, resolution, method, expected):
    assert match_pairs(hla1_1, hla1_2, hla2_1, hla2_2, resolution, method) == expected
