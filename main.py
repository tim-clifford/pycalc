import chk,calc,test,cnst
import math
#NOTE: infix operator control characters must be one character
OPERATORS = [
    [
        # Infix
        [['^'],lambda a,b: a**b],
        [['x','*'],lambda a,b: a*b],
        [['/'],lambda a,b: a/b],
        [['+'],lambda a,b: a+b],
        [['-'],lambda a,b: a-b],
    ],[
        
        # Prefix. Parentheses recommended as given highest priority. 
        # Using math functions temporarily.

        # Radians only. You can use fractions of tau. There is no support for the inferior circle constant
        [['asin','sin-1','arcsin'],lambda a: math.asin(a)],
        [['acos','cos-1','arccos'],lambda a: math.acos(a)],
        [['atan','tan-1','arctan'],lambda a: math.atan(a)],
        [['sin'],lambda a: math.sin(a)],
        [['cos'],lambda a: math.cos(a)],
        [['tan'],lambda a: math.tan(a)],
        
    ]
]
BRACKETS = [
    ['{','}'],
    ['[',']'],
    ['(',')'],
]
brk = "".join("".join(a) for a in BRACKETS)
ops = "".join("".join(a[0]) for a in OPERATORS[0]) 

if __name__ == "__main__":
    try:
        test.run_tests()
    except AssertionError: 
        print("This program is broken, don't bother.")
        raise SystemExit
    while True:
        try:
            inp = input("Enter an expression: ")
            if True:#chk.check(inp):
                out = calc.parse_brackets(inp)
                if out: print(out)
                else: print("Math Error")
            else: print("Syntax Error")
        except KeyboardInterrupt:
            print()
            raise SystemExit

