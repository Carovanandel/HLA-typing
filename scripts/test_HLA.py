from HLA import HLA
import pytest

#test class initialization
def test_HLA():
    hla = HLA('A', '01')

    assert hla.gene == 'A'
    assert hla.allele == '01'
    assert hla.protein is None

    assert str(hla) == "HLA-A*01"

#test __eq__ 
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

#test string representation with str()
as_str = [
    (HLA('A'), "HLA-A"),
    (HLA('A', '01'), "HLA-A*01"),
    (HLA('A', '01', '05'), "HLA-A*01:05"),
]
@pytest.mark.parametrize("hla, expected", as_str)
def test_print(hla, expected):
    assert str(hla) == expected

#tests from_str method to create a class object from a string
from_str = [
    ("HLA-A", HLA("A")),
    ("HLA-ABCDE", HLA("ABCDE")),
    ("HLA-A*10", HLA("A", "10")),
    ("HLA-A*02:101", HLA("A", "02", "101")),
    ("0", HLA(None)),
    ("HLA-DRB1", HLA("DRB1")),
    ("HLA-DRB1*13:01:01:02", HLA("DRB1", "13", "01", "01", "02")),
    ("HLA-A*24:09N", HLA(gene="A", allele="24", protein="09", suffix="N")),
    ("HLA-A*30:14L", HLA(gene="A", allele="30", protein="14", suffix="L")),
    ("HLA-A*24:02:01:02L", HLA(gene="A", allele="24", protein="02", synonymous="01", noncoding="02", suffix="L")),
    ("HLA-B*44:02:01:02S", HLA(gene="B", allele="44", protein="02", synonymous="01", noncoding="02", suffix="S")),
    ("HLA-A*32:11Q", HLA(gene="A", allele="32", protein="11", suffix="Q")),
]
@pytest.mark.parametrize("string, hla", from_str)
def test_hla_from_string(string, hla):
    assert HLA.from_str(string) == hla
    assert str(hla) == string

match = [
    (HLA('A', '01'), HLA('A', '01'), 2, True),
    (HLA('A', '01', '01'), HLA('A', '01', '01'), 2, True),
    (HLA('A', '01', '01'), HLA('A', '01', '02'), 2, False),
    (HLA('A', '01', '01'), HLA('A', '01'), 2, True),
    (HLA('A', '01'), HLA('A', '01', '01'), 2, True),
    (HLA('A', '01'), HLA('A', '01', '01'), 1, False),
    (HLA(None), HLA('A', '01', '01'), 2, False),
    (HLA(None), HLA(None), 1, True),
    (HLA(None), HLA(None), 2, True),
]

@pytest.mark.parametrize("hla, hla2, method, expected", match)
def test_match(hla, hla2, method, expected):
    assert hla.match(hla2, method) == expected
    assert hla2.match(hla, method) == expected
