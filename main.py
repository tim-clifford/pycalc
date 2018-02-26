import chk,calc,test,cnst,trig
import sys # Surely I am allowed to get command line options
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
    if not ("--quiet" in sys.argv or "-q" in sys.argv):
        print("""\
Type calculations exactly as you'd expect.
To switch between SCI and EXACT modes enter "mode".
For the last answer use "ans", to clear history "clr"
To kill this message on launch use the option -q or --quiet""")
    try:
        test.run_tests()
    except AssertionError: 
        print("This program is broken, don't bother.")
        raise SystemExit
    exact = True
    try: 
        history = open("history.txt").read().split("\n")
    except:
        open("history.txt","a").write("")
        history = []
    while True:
        try:
            inp = input("> ").lower()
            chk.make_sure_they_understand_which_circle_constant_is_correct(inp)
            if inp in ["q","q()","exit","exit()","quit","quit()"]: raise SystemExit
            elif inp == "mode": exact = not exact
            elif inp == "clr": open("history.txt","w").write("1\n")
            else:
                inp = str(chk.history(inp))
                out = calc.parse_brackets(inp)
                if out[1] != "": # don't want to print empty lines
                    try: 
                        out[1].simplify()
                        if float(out[1]) < 10**-15: print(0) # below the accuracy and is annoying
                        elif exact: print(out[1])
                        else: print(float(out[1]))
                    except (ValueError, AttributeError): print(out[1]) # errors
        except (KeyboardInterrupt, EOFError):
            print()
            raise SystemExit
        except Exception as e:
            print("Unknown Error. Logged.")
            print(e,file=open("errorlog.txt","w"))

