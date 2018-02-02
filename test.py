import chk,calc,cnst
import math
def run_tests():
    assert chk.check("1+23x1^3/2^1") == True
    assert chk.check("+1x2") == False
    assert chk.check(r"{1x5} + [5*3]") == True
    assert chk.check("1++2") == False
    assert chk.check("1+a^1") == False
    assert float(calc.evaluate("1.2^3+2x9")) == 19.728
    assert float(calc.parse_brackets("{1+5}^5-[1x5]")) == 7771
    assert not calc.parse_brackets("(1x2]")
    assert not calc.parse_brackets("[1x2+{3^4]}")
    assert chk.check("4")
    assert chk.check("1.2")
    assert calc.evaluate(cnst.replace_constants("tau")) == str(2*math.pi)
    assert calc.parse_brackets(cnst.replace_constants("e^(e^tau)")) == str(math.e**(math.e**(2*math.pi)))

if __name__ == "__main__": run_tests()