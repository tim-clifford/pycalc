# Python's dynamic nature makes things harder (if I want them safe) here. Ugh.

import cnst
class Exact:
    def __init__(self,a = 1,const = [0]*len(cnst.CONSTANTS)):
        self.a = a
        self.const = const
    def isSimple(self):
        if self.const == [0]*len(cnst.CONSTANTS): return True
        return False
    def ToString(self):
        if self.a == 0: return "0"
        elif self.a == 1 and self.const != [0]*len(cnst.CONSTANTS): acc = ""
        else: 
            if self.a == int(self.a):
                acc = str(int(self.a))
            else: acc = str(self.a)
        for i,j in enumerate(self.const):
            if j == 0: continue
            elif j == 1: acc += cnst.CONSTANTS[i][2]
            else: acc += "{0}^{1}".format(cnst.CONSTANTS[i][2],j)
        return acc
    def ToFloat(self):
        acc = self.a
        for i,j in enumerate(self.const):
            acc *= cnst.CONSTANTS[i][1] ** j
        return acc
    def mult(ext1,ext2):
        return Exact(ext1.a*ext2.a,[x+y for x,y in zip(ext1.const,ext2.const)])
    def negate(ext):
        return Exact(-ext.a,ext.const)
class ExactSum:
    def __init__(self,exacts):
        if isinstance(exacts,list):
            if all(isinstance(x,Exact) for x in exacts):
                self.list = exacts
                return
        raise TypeError("Invalid list")
    def Add(extS1,extS2):
        # These shouldn't be large, so we can get away with O(n^2)
        acc = []
        l1 = extS1.list[:]
        l2 = extS2.list[:]
        for i in l1:
            for j in l2:
                if i.const == j.const:
                    acc.append(Exact(i.a + j.a,i.const))
                    i.pop()
                    j.pop()
        return acc + l1 + l2
    def negate(extSum):
        return ExactSum([Exact.negate(x) for x in extSum.list])
    def ToFloat(self):
        return sum([x.ToFloat() for x in self.list])
    def __float__(self): return self.ToFloat()
    def __int__(self): return int(self.ToFloat())
class num:
    '''
    the numerator is an unevaluated sum of exact values, held by the ExactSum class
    '''
    exact = True
    def __init__(self,numerator=1,denominator=1,constB=[0]*len(cnst.CONSTANTS)):
        if isinstance(numerator,int) or isinstance(numerator,float):
            self.a = ExactSum([Exact(numerator)])
        elif isinstance(numerator,Exact):
            self.a = ExactSum([numerator])
        elif isinstance(numerator,ExactSum):
            self.a = numerator
        elif isinstance(numerator,num):
            if denominator == 1 and constB == [0]*len(cnst.CONSTANTS):
                self.a = numerator.a
                self.b = numerator.b
            else: raise ValueError
        else: 
            raise TypeError
        if not isinstance(numerator,num): self.b = Exact(denominator,constB)
    def simplify(self):
        if not self.exact: return False 
        # simplify the top sum
        # we are changing i and j dynamically so for loops won't do.
        i,j = len(self.a.list),0
        while True:
            i -= 1
            if i < 0: break
            while True:
                if j >= i: break
                if self.a.list[i].const == self.a.list[j].const:
                    self.a.list[j].a += self.a.list[i].a
                    try: self.a.list = self.a.list[:i]+self.a.list[i+1:]
                    except IndexError: self.a.list = self.a.list[:i]
                    i-=1
                j += 1
        # find and remove common factors
        common = []
        for i in range(len(cnst.CONSTANTS)):
            common.append(min(x.const[i] for x in self.a.list))
            for j in self.a.list: j.const[i] -= min(common[i],self.b.const[i])
            self.b.const[i] -= min(common[i],self.b.const[i])
        for i in range(2,int(abs(min(*(x.a for x in self.a.list),self.b.a)))+1):
            if all(x.a%i == 0 for x in self.a.list) and self.b.a%i == 0:
                for x in self.a.list: x.a //= i
                self.b.a //= i
        return True
    def ToString(self):
        if self.exact:
            strA = "+".join(x.ToString() for x in self.a.list).replace("+-","-")
            strB = self.b.ToString()
            if self.b.a == 1 and self.b.const == [0]*len(cnst.CONSTANTS):
                return strA
            else:
                return "{0}\n{1}\n{2}".format(strA,"-"*max(len(strA),len(strB)),strB)
        else:
            return str(self.ToFloat())
    def __str__(self): return self.ToString()
    def ToFloat(self):
        acc = sum(x.ToFloat() for x in self.a.list) / self.b.a
        for i,j in enumerate(self.b.const): acc /= (cnst.CONSTANTS[i][1] ** j)
        return acc
    def __float__(self): return self.ToFloat()
    def __int__(self): return int(self.ToFloat())
    def add(num1,num2):
        numSum = num()
        numSum.b = Exact.mult(num1.b,num2.b)
        aList = []
        for i in num1.a.list:
            aList.append(Exact.mult(i,num2.b))
        for i in num2.a.list:
            aList.append(Exact.mult(i,num1.b))
        numSum.a = ExactSum(aList)
        numSum.simplify()
        return numSum
    def __add__(self,other):
        if not isinstance(other,num):
            return num.add(self,num(other))
        else: return num.add(self,other)
    def negate(n):
        return num(ExactSum.negate(n.a),n.b.a,n.b.const)
    def __neg__(self):
        return num.negate(self)
    def sub(num1,num2):
        return num.add(num1,num.negate(num2))
    def __sub__(self,other):
        if not isinstance(other,num):
            return num.sub(self,num(other))
        else: return num.sub(self,other)
    def mult(num1,num2):
        numMult = num()
        numMult.b = Exact.mult(num1.b,num2.b)
        aList = []
        for i in num1.a.list:
            for j in num2.a.list:
                aList.append(Exact.mult(i,j))
        numMult.a = ExactSum(aList)
        numMult.simplify()
        return numMult
    def __mul__(self,other):
        if not isinstance(other,num):
            return num.mult(self,num(other))
        else: return num.mult(self,other)
    '''
    def __imul__(self,other):
        if not isinstance(other,num):
            self = num.mult(self,num(other))
        else: self = num.mult(self,other)
    '''
    def power(num1,num2):
        if float(num2) == int(num2):
            numPower = num()
            for i in range(abs(int(num2))):
                numPower = numPower * num1
            if num2 < 0: return 1/numPower
            else: return numPower
        else:
            numPower = num(float(num1)**float(num2))
            numPower.exact == False
            return numPower

    def __pow__(self,other):
        if not isinstance(other,num):
            return num.power(self,num(other))
        else:
            return num.power(self,other)
    def div(num1,num2):
        # This is hard because we have to rearrange Exact/ExactSum into ExactSum/Exact
        # For now it will be handled partially numerically
        if num2.ToFloat() == 0:
            raise DivisionByZeroError
        invNum2 = num()
        invNum2.a.list[0] = num2.b
        if len(num2.a.list) > 1:
            invNum2.b = num2.a.ToFloat()
            ext = False
        else: 
            invNum2.b = num2.a.list[0]
            ext = True
        m = num.mult(num1,invNum2)
        m.exact = ext
        return m
    def __truediv__(self,other):
        if not isinstance(other,num):
            return num.div(self,num(other))
        else: return num.div(self,other)
    def __rtruediv__(self,other):
        return num.div(num(other),self)
    def __eq__(self,value):
        if isinstance(value,float) or isinstance(value,int) or isinstance(value,num):
            return float(self) == float(value)
        elif isinstance(value,str):
            return str(self) == value
        else:
            return False
    def __lt__(self,value):
        return float(self) < float(value)
if __name__ == "__main__":
    a = num(1.0,1.0,[0,0])
    b = num(3.0,1.0,[0,0])
    c = a/b
    print(str(c))
   #print(c.ToString())