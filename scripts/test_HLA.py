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
    ("HLA-DRB1", HLA("DRB1")),
    ("HLA-DRB1*13:01:01:02", HLA("DRB1", "13", "01", "01", "02")),
    ("HLA-A*24:09N", HLA(gene="A", allele="24", protein="09", suffix="N")),
    ("HLA-A*30:14L", HLA(gene="A", allele="30", protein="14", suffix="L")),
    ("HLA-A*24:02:01:02L", HLA(gene="A", allele="24", protein="02", synonymous="01", noncoding="02", suffix="L")),
    ("HLA-B*44:02:01:02S", HLA(gene="B", allele="44", protein="02", synonymous="01", noncoding="02", suffix="S")),
    ("HLA-A*32:11Q", HLA(gene="A", allele="32", protein="11", suffix="Q")),
    #("0", HLA(None)),
]
@pytest.mark.parametrize("string, hla", from_str)
def test_hla_from_string(string, hla):
    assert HLA.from_str(string) == hla
    assert str(hla) == string

def test_invalid_HLA_string() -> None:
    with pytest.raises(ValueError):
        HLA.from_str("hla25")


match = [
    (HLA('A', '01'), HLA('A', '01'), 2, True),
    (HLA('A', '01', '01'), HLA('A', '01', '01'), 2, True),
    (HLA('A', '01', '01'), HLA('A', '01', '02'), 2, False),
    (HLA('A', '01', '01'), HLA('A', '01'), 2, False),
    (HLA('A', '01'), HLA('A', '01', '01'), 2, False),
    (HLA('A', '01'), HLA('A', '01', '01'), 1, True),
    (HLA(None), HLA('A', '01', '01'), 2, False),
    (HLA(None), HLA(None), 1, True),
    (HLA(None), HLA(None), 2, True),
]

@pytest.mark.parametrize("hla, hla2, resolution, expected", match)
def test_match(hla, hla2, resolution, expected):
    assert hla.match(hla2, resolution) == expected
    assert hla2.match(hla, resolution) == expected

fields_list = [
    (HLA('A','01','02','03','04','S'), ['A','01','02','03','04','S']),
    (HLA('B','03','02'), ['B','03','02',None,None,None]),
    (HLA(None), [None,None,None,None,None,None]),
    (HLA(gene='A', allele='24', protein='09', suffix='N'), ['A','24','09',None,None,'N']),
]

@pytest.mark.parametrize("hla, expected", fields_list)
def test_fields(hla, expected):
    assert hla.fields() == expected

fields_list_from_str = [
    ('HLA-A*01:02:03:04S', ['A','01','02','03','04','S']),
    ('HLA-B*03:02', ['B','03','02',None,None,None]),
    ('HLA-A*24:09N', ['A','24','09',None,None,'N']),
    #('0', [None,None,None,None,None,None]),
]

@pytest.mark.parametrize("hla, expected", fields_list_from_str)
def test_fields_from_str(hla, expected):
    assert HLA.fields_from_str(hla) == expected

match_test=[
    (HLA('A','01','02','03','04','S'), HLA('A','01','02','03','04','S'), None, True),
    (HLA('A','01','02','03','04','S'), HLA('A','01','02','03','04','S'), 0, True),
    (HLA('A','01','02','03','04','S'), HLA('A','01','02','03','04','S'), 1, True),
    (HLA('A','01','02','03','04','S'), HLA('A','01','02','03','04','S'), 2, True),
    (HLA('A','01','02','03','04','S'), HLA('A','01','02','03','04','S'), 5, True),
    (HLA('A','01','02','03','04','S'), HLA('A','01','02','03','04'), 5, False),
    (HLA('A','01','02'), HLA('A','01','06'), 1, True),
    (HLA('A','01','02'), HLA('A','01','06'), 2, False),
    (HLA(None), HLA(None), 3, True),
    (HLA('A','01'), HLA('A','01','06'), None, True),
    (HLA(None), HLA('A','01','01'), None, True),
    (HLA(None), HLA('A','01','01'), 2, False),
]

@pytest.mark.parametrize('self, other, resolution, expected', match_test)
def test_match(self, other, resolution, expected):
    assert self.match(other, resolution) == expected
    assert other.match(self, resolution) == expected
