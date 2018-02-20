import chk,calc,test,cnst,trig
#NOTE: infix operator control characters must be one character
OPERATORS = [
    [
        # Infix
        [['^'],lambda a,b: a**b],
        [['C'],trig.comb],
        [['x','*'],lambda a,b: a*b],
        [['/'],lambda a,b: a/b],
        [['+'],lambda a,b: a+b],
        [['-'],lambda a,b: a-b],
    ],[
        # Prefix. Second highest priority behind postfix. 
        # Using series expansions for trig

        # Radians only for trig. You can use fractions of tau. Using the inferior circle constant will exit the calculator
        [['asin','arcsin'],trig.arcsin],
        [['acos','arccos'],trig.arccos],
        [['atan','arctan'],trig.arctan],
        [['sin'],trig.sin],
        [['cos'],trig.cos],
        [['tan'],trig.tan], 
        
    ],[
        # Postfix. Highest priority
        [['!'],trig.fact]
    ],[
        # Bracketed multi parameter functions. Not implemented. Format name, number of operands, function
        [['log'],2,""],
        [['']]
    ]
]
BRACKETS = [
    ['{','}'],
    ['[',']'],
    ['(',')'],
]
brk = "".join("".join(a) for a in BRACKETS)
ops = "".join("".join(a[0]) for a in OPERATORS[0])
pfx = sum([a[0] for a in OPERATORS[1]],[])
ptx = sum([a[0] for a in OPERATORS[2]],[])


if __name__ == "__main__":
    try:
        test.run_tests()
    except AssertionError: 
        print("This program is broken, don't bother.")
        raise SystemExit
    while True:
        try:
            inp = input("> ")
            chk.make_sure_they_understand_which_circle_constant_is_correct(inp)
            if inp in ["q","q()","exit","exit()","quit","quit()"]: raise SystemExit
            out = calc.parse_brackets(inp)
            if out[1] != "": print(out[1])

        except (KeyboardInterrupt, EOFError):
            print()
            raise SystemExit

