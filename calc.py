import main, cnst
def parse_brackets(string):
    op = [a[0] for a in main.BRACKETS]
    cl = [a[1] for a in main.BRACKETS]
    for i in main.brk:
        if i in string: break
    else: 
        try: return evaluate(string)
        except: 
            return False
    j,l = 0,""
    for i,c in enumerate(string):
        if c in "".join(op):
            j,l = i,c
        elif c in "".join(cl):
            if l == "": return False
            elif c != cl[op.index(l)]: 
                return False
            return parse_brackets(string[:j] + parse_brackets(string[j+1:i]) + string[i+1:])

def evaluate(string):
    string = cnst.replace_constants(string)
    acc = string
    # Prefix first
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