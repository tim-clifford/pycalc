import chk,calc,cnst,trig,math,num
def run_tests():
    assert chk.check("1+23x1^3/2^1")
    assert not chk.check("+1x2")
    assert chk.check("1x5 + 5*3")
    assert not chk.check("1++2")
    assert not chk.check("1+a^1")
    assert trig.abs(float(calc.evaluate("sin-1")) - math.sin(-1)) < trig.TOLERANCE
    assert calc.evaluate("2*tau^3+2x9") == 2*(2*math.pi)**3+18
    assert float(calc.parse_brackets("{1+5}^5-[1x5]")[1]) == 7771
    assert not calc.parse_brackets("(1x2]")[0]
    assert not calc.parse_brackets("[1x2+{3^4]}")[0]
    assert chk.check("4")
    assert chk.check("1.2")
    assert float(calc.evaluate(cnst.replace_constants("tau"))) == 2*math.pi
    assert float(calc.parse_brackets(("e^(e^tau)"))[1]) == math.e**(math.e**(2*math.pi))
    assert float(calc.parse_brackets("(1-3)+4")[1]) == 2
    assert float(calc.evaluate("cos1 + 2")) == math.cos(1) + 2
    assert float(calc.parse_brackets("cos (tau / 4)")[1])
    assert float(calc.evaluate("asin 1"))
    assert chk.check("tau")
    assert calc.parse_brackets("cos -1")[0]
    trig.test()
    assert calc.parse_brackets("a")[1] == "Syntax Error"
    assert float(calc.evaluate("1!")) == 1
    assert calc.parse_brackets("2-1!")[0]
    assert calc.evaluate("tau*3*4/tau") == 12
    assert calc.parse_brackets("(tau/e) * [e/tau]")
    assert calc.parse_brackets("2*(2*(tau/4))")[0]
if __name__ == "__main__": run_tests()