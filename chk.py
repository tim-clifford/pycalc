import main
from cnst import CONSTANTS
cnst = [a[0] for a in CONSTANTS]


def make_sure_they_understand_which_circle_constant_is_correct(string):
    if "pi" in string:
        print("π is the inferior circle constant, learn to use τ before coming back.\nGoodbye.")
        raise SystemExit

def history(string):
    if "ans" in string:
        s = string.replace("ans","("+open("history.txt").readlines()[-1][:-1]+")")
    else: s = string
    if s[0] == "(" and s[-1] == ")": s = s[1:-1]
    open("history.txt","a").write(s+"\n")
    return s

def check(string):
    '''
    Called by calc.evaluate, so brackets are handled separately.

    regex:
    ([`prefix`]?-?[0-9.]+|[`constants`][`operators`]|$)* (probably)
    
    For reference:
    0 (
    1     [`prefix`]?
    2     -?
    3     [0-9.]+
    4    |[`constants`]
    5     [`postfix`]?
    6     [`operators`]
    7    |$
    8 )?
    
    '''
    string = string.replace(" ","")
    # couldn't get regex module to work. Plus, no importing, right?
    index = 0
    if string == "": return True # 8
    while True: # 0/8
        for prefix in main.pfx: # 1
            if len(string[index:]) > len(prefix) and string[index:index+len(prefix)] == prefix: #1
                index += len(prefix)
                break
        if string[index] == '-': #2
            index += 1
        for const in cnst: #4
            if len(string[index:]) >= len(const) and string[index:index+len(const)] == const:
                index += len(const)
                if index == len(string): return True # 7
                break
        else:
            if string[index] in "0123456789.": #3
                for i,j in enumerate(string[index:]):
                    if not j in "0123456789.":
                        index += i
                        break
                else: return True # 7
            else: return False
        if string[index] in main.ptx:
            index += 1
        if index == len(string): return True
        if string[index] in main.ops: # 6
            index += 1; continue
        else: return False