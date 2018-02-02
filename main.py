import chk,calc,test,cnst
#NOTE: operator control characters must be one character (as of now)
OPERATORS = [
    [['^'],lambda a,b: a**b],
    [['x','*'],lambda a,b: a*b],
    [['/'],lambda a,b: a/b],
    [['+'],lambda a,b: a+b],
    [['-'],lambda a,b: a-b]
]
BRACKETS = [
    ['{','}'],
    ['[',']'],
    ['(',')'],
]
brk = "".join("".join(a) for a in BRACKETS)
ops = "".join("".join(a[0]) for a in OPERATORS) 

if __name__ == "__main__":
    try:
        test.run_tests()
    except AssertionError: 
        print("This program is broken, don't bother.")
        raise SystemExit
    while True:
        try:
            inp = input("Enter an expression: ")
            inp = cnst.replace_constants(inp)
            if chk.check(inp):
                out = calc.parse_brackets(inp)
                if out: print(out)
                else: print("Calculation Failed")
            else: print("Invalid Expression")
        except KeyboardInterrupt:
            print()
            raise SystemExit

