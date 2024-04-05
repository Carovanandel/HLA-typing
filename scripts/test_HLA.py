from HLA import HLA
import pytest


def test_HLA():
    hla = HLA('A', '01')

    assert hla.gene == 'A'
    assert hla.allele == '01'
    assert hla.protein is None

    assert str(hla) == "HLA-A*01"


identical = [
    (HLA('A', '01'), HLA('B', '01'), False),
    (HLA('A', '01'), HLA('A', '01'), True),
    (HLA('A', '01'), HLA('A', '02'), False),
    (HLA('A'), HLA('A'), True),
    (HLA('A', '01'), HLA('A', '01', '01'), False),
]

@pytest.mark.parametrize("x, y, expected", identical)
def test_HLA_identical(x, y, expected):
    assert (x == y) == expected


as_str = [
    (HLA('A'), "HLA-A"),
    (HLA('A', '01'), "HLA-A*01"),
    (HLA('A', '01', '05'), "HLA-A*01:05"),
]
@pytest.mark.parametrize("hla, expected", as_str)
def test_print(hla, expected):
    assert str(hla) == expected


from_str = [
    ("HLA-A", HLA("A")),
    ("HLA-ABCDE", HLA("ABCDE")),
    ("HLA-A*10", HLA("A", "10")),
    ("HLA-A*02:101", HLA("A", "02", "101")),
]
@pytest.mark.parametrize("string, hla", from_str)
def test_hla_from_string(string, hla):
    assert HLA.from_str(string) == hla
    assert str(hla) == string
