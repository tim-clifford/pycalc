import main, cnst, chk
def parse_brackets(string):
    op = [a[0] for a in main.BRACKETS]
    cl = [a[1] for a in main.BRACKETS]
    for i in main.brk:
        if i in string: break
    else: 
        try: return True,evaluate(string)
        except ValueError:
            return False,"Syntax Error"
        except: 
            return False,"Calculation Error"
    j,l = 0,""
    for i,c in enumerate(string):
        if c in "".join(op):
            j,l = i,c
        elif c in "".join(cl):
            if l == "": return False,"Bracket Error (closed before opened)"
            elif c != cl[op.index(l)]: 
                return False,"Bracket Error (mismatched)"
            try:
                return True,parse_brackets(string[:j] + parse_brackets(string[j+1:i])[1] + string[i+1:])[1]
            except TypeError:
                return False,"Bracket Error (other)"
    return False,"Bracket Error (not closed)"
def evaluate(string):
    if not chk.check(string): raise ValueError
    string = cnst.replace_constants(string)
    acc = string.replace(" ","")
    # Postfix first
    for typ in main.OPERATORS[2]:
        for op in typ[0]:
            acc = acc.split(op)
            while len(acc) > 1:
                pre = acc[0]
                post = "".join(acc[1:])
                p,j = [""],0
                for i in pre:
                    if i in main.ops:
                        p.append(i); p.append(""); j += 2
                    else: p[j] += i
                pre = p
                while pre[-1] == '' and len(pre) > 1: pre = list(pre[:-1])
                acc = str("{:.20f}".format(typ[1](float(pre[-1])))) + post
                if len(pre) > 1: acc = "".join(pre[:-1]) + acc
                acc = acc.split(op)
            acc = acc[0]
    # then prefix
    for typ in main.OPERATORS[1]:
        for op in typ[0]:
            acc = acc.split(op)
            while len(acc) > 1:
                pre = acc[0]
                post = "".join(acc[1:])
                p,j = [""],0
                for i in post:
                    if i in main.ops:
                        p.append(i); j += 1
                    else: p[j] += i
                post = p
                while post[0] == '' and len(post) > 1: post = list(post[1:])
                acc = pre + str("{:.20f}".format(typ[1](float(post[0]))))
                if len(post) > 1: acc += "".join(post[1:])
                acc = acc.split(op)
            acc = acc[0]
    
    # Now infix
    for typ in main.OPERATORS[0]:
        for op in typ[0]:
            acc = acc.split(op)
            if len(acc) > 1:
                # get nums
                tmp = acc[0]
                pre = ""
                for i in main.ops:
                    tmp = str((tmp)).replace(" ","")
                    sp = tmp.split(i)
                    num0 = sp[-1]
                    if (len(sp)>1): pre += "".join(sp[:-1]) + i
                    tmp = num0
                # Fixing the annoying edge case where '-' isn't a function
                if pre == '-':
                    num0 = '-'+num0
                    pre = ""
                tmp = acc[1]
                post = ""
                for i in main.ops:
                    tmp = str((tmp)).replace(" ","")
                    sp = tmp.split(i)
                    num1 = sp[0]
                    if (len(sp)>1): post = i + "".join(sp[1:]) + post
                    tmp = num1
                # Here we go again...
                if num0 == '' and op == '-':
                    num0 = '0'
                acc = pre+str("{:.20f}".format(typ[1](float(num0),float(num1))))+post
            else: acc = acc[0]
    return acc