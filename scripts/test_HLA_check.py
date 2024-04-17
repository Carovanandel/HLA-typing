import pytest
import sys
from HLA import HLA

#bypass sys.argv assertion error in HLA_check.py
sys.argv = ['HLA_check.py','scripts/test_files/testoutput_lab.csv', 
            'scripts/test_files/testoutput_tool.csv', '2', 'all']
from HLA_check import get_hla_list, check_match

hla_output = [
    ('HLA-A*01:01', [HLA('A','01','01')]),
    ('0', [HLA(None)]),
    ('HLA-A*01:01/HLA-A*01:02', [HLA('A','01','01'),HLA('A','01','02')]),
    ('HLA-B*01:01/HLA-B*01', [HLA('B','01','01'), HLA('B','01')]),
    ('HLA-C*01:01N', [HLA('C','01','01',None,None,'N')]),
]

@pytest.mark.parametrize("hla, expected", hla_output)
def test_get_hla_list(hla, expected):
    assert get_hla_list(hla) == expected

match = [
    ([HLA('A','01','01')],  [HLA('A','02','02')], [HLA('A','01','01')], [HLA('A','02','02')], 0, 2),
    ([HLA('A','01','01')], [HLA('A','02','02')], [HLA('A','01','04')], [HLA('A','02','02')], 0, 1),
    ([HLA('A','01','01')], [HLA('A','02','02')], [HLA('A','01','04')], [HLA('A','02','04')], 0, 0),
    ([HLA('A','01','01')], [HLA('A','02','02')], [HLA('A','02','02')], [HLA('A','01','01')], 0, 2),
    ([HLA('A','01','01'), HLA('A','01','04')], [HLA('A','01','04')], [HLA('A','01','04')], [HLA('A','02','02')], 0, 1),
    ([HLA('A','01','01'), HLA('A','01','02')], [HLA(None)], [HLA('A','01','01')], [HLA('A','01','02')], 0, 1),
    ([HLA('A','01','01'), HLA('A','01','02')], [HLA('A','01','02'), HLA('A','01','01')], [HLA('A','01','01')], [HLA('A','01','02')], 0, 2),
]

### Turned of this test for now
# @pytest.mark.parametrize("hla1_1, hla1_2, hla2_1, hla2_2, allele_score, expected", match)
# def test_check_match(hla1_1, hla1_2, hla2_1, hla2_2, allele_score, expected):
#     assert check_match(hla1_1, hla1_2, hla2_1, hla2_2, allele_score) == expected

