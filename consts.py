from note import Note as N

MAJOR_INTERVALS = [2,2,1,2,2,2,1]
PHRYGIAN_INTERVALS = [1,2,2,2,1,2,2]
ORDER = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
NUMERALS = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}
VRANGE=[[N("c", 0,4), N("a", 0,5)], [N("g", 0,3), N("e", 0,5)], [N("e", 0,3), N("a", 0,4)], [N("f", 0,2), N("d", 0,4)]]
PREFERRED = [N("a",1,4),N("f",0,4),N("b",0,3),N("e",0,3)]