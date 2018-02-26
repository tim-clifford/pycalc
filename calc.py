import main, cnst, chk, num
def parse_brackets(inp):
    op = [a[0] for a in main.BRACKETS]
    cl = [a[1] for a in main.BRACKETS]
    if isinstance(inp,list):
        brkTestStr = "".join(str(x) for x in inp)
    elif isinstance(inp,str): brkTestStr = inp
    for i in main.brk:
        if i in brkTestStr: break
    else: 
        try: return True,evaluate(inp)
        except ValueError:
            return False,"Syntax Error"
        except:
            return False,"Calculation Error"
    # Check it separately first as the list will make things hard.
    j,l = 0,""
    for c in brkTestStr.replace(" ",""):
        if c in "".join(op):
            l = c
        elif c in "".join(cl):
            if l == "": return False,"Bracket Error (closed before opened)"
            elif c != cl[op.index(l)]: 
                return False,"Bracket Error (mismatched)"

    if not isinstance(inp,list): inp = [inp]
    asnum = []
    j,l,m = 0,"",0
    for k,string in enumerate(inp):
        if not isinstance(string,str): 
            asnum.append(string); continue
        string = string.replace(" ","")
        opened = False # don't cause an error if there are no brackets
        for i,c in enumerate(string):
            if c in "".join(op):
                opened = True
                j,l,m = i,c,k
            elif c in "".join(cl):
                opened = False
                #if l == "" or c != cl[op.index(l)]: continue
                try:
                    if m == k:
                        toParse = [string[:j],parse_brackets(string[j+1:i])[1],string[i+1:]]
                        toParse = [x for x in toParse if x != ""]
                        return parse_brackets(asnum + toParse)
                        break
                    else:
                        toParse = [inp[:m],inp[m][:j],parse_brackets([inp[m][j+1:],*inp[m+1:k],string[:i]])[1],string[i+1:]]
                        toParse = [x for x in toParse if x != "" and x != []]
                        return parse_brackets(toParse)
                except TypeError as e:
                    return False,"Bracket Error (other)"
        if opened and k == len(inp)-1:
            return False,"Bracket Error (not closed)"
def evaluate(inp):
    if isinstance(inp,str):
        if not chk.check(inp): raise ValueError
        inp = [inp.replace(" ","")]
    elif isinstance(inp,list):
        if not all(isinstance(x,num.num) or isinstance(x,str) for x in inp):
            raise TypeError
    else: raise TypeError
    asnum = []
    for string in inp:
        if string == "": continue
        if isinstance(string,num.num): asnum.append(string)
        else:
            i = 0
            isnum = False
            while True:
                if string[i] in "0123456789.":
                    if isnum: asnum[-1] += string[i]
                    else: 
                        asnum.append(string[i])
                        isnum = True
                    i += 1
                else:
                    if isnum:
                        asnum[-1] = num.num(float(asnum[-1]))
                        isnum = False
                    for j,x in enumerate(cnst.CONSTANTS):
                        if i + len(x[0]) <= len(string) and string[i:i+len(x[0])] == x[0]:
                            asnum.append(num.num(num.Exact(1,[0]*j+[1]+[0]*(len(cnst.CONSTANTS)-j-1))))
                            i += len(x[0]); break
                    for x in list(main.ops) + main.pfx + main.ptx:
                        if i + len(x) <= len(string) and string[i:i+len(x)] == x:
                            asnum.append(string[i:i+len(x)])
                            i += len(x); break
                if i >= len(string): 
                    if isnum: asnum[-1] = num.num(float(asnum[-1]))
                    break
    # goddamn edge cases
    for i,j in enumerate(asnum):
        if j == '-' and (i == 0 or not isinstance(asnum[i-1],num.num)):
            asnum[i+1] = -asnum[i+1]
            asnum = asnum[:i] + asnum[i+1:]
    # Postfix first
    for typ in main.OPERATORS[2]:
        for op in typ[0]:
            for i,j in enumerate(asnum):
                if isinstance(j,str) and j == op:
                    asnum = asnum[:i-1] + [num.num(typ[1](asnum[i-1]))] + asnum[i+1:]
    # then prefix
    for typ in main.OPERATORS[1]:
        for op in typ[0]:
            for i,j in enumerate(asnum):
                if isinstance(j,str) and j == op:
                    try:
                        asnum = asnum[:i] + [num.num(typ[1](asnum[i+1]))] + asnum[i+2:]
                    except IndexError:
                        asnum = asnum[:i] + [num.num(typ[1](asnum[i+1]))]
    # Now infix
    for typ in main.OPERATORS[0]:
        for op in typ[0]:
            # We can't use a classic for...enumerate as we are changing the list as we iterate.
            i = 0
            while True:
                if i >= len(asnum): break
                j = asnum[i]
                if isinstance(j,str) and j == op:
                    if len(asnum[:i]) > 1:
                        if len(asnum[i+1:]) > 1:
                            asnum = asnum[:i-1] + [num.num(typ[1](asnum[i-1],asnum[i+1]))] + asnum[i+2:]
                        else:
                            asnum = asnum[:i-1] + [num.num(typ[1](asnum[i-1],asnum[i+1]))]
                    elif len(asnum[i+1:]) > 1:
                        asnum = [num.num(typ[1](asnum[i-1],asnum[i+1]))] + asnum[i+2:]
                    else:
                        asnum = [num.num(typ[1](asnum[i-1],asnum[i+1]))]
                else: i += 1 
    if len(asnum) == 1: return asnum[0]
    else: raise ArithmeticError

if __name__ == "__main__": print(evaluate("e/tau"))