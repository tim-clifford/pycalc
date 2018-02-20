# Python's dynamic nature makes things harder (if I want them safe) here. Ugh.

import cnst
class Exact:
    def __init__(self,a = 1,const = [0]*len(cnst.CONSTANTS)):
        self.a = a
        self.const = const
class ExactSum:
    def __init__(self,exacts):
        if isinstance(exacts,list):
            if all(isinstance(x,Exact) for x in exacts):
                self.list = exacts
                return
        raise Exception("Invalid list")
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
class num:
    '''
    the numerator is an unevaluated sum of exact values, held by the ExactSum class
    '''
    exact = True
    def __init__(self,numerator=1,denominator=1,constB=[0]*len(cnst.CONSTANTS)):
        if isinstance(numerator,int) or isinstance(numerator,float):
            self.a = [ExactPart(numerator)]
        if isinstance(numerator,Exact):
            self.a = ExactSum([numerator])
        if isinstance(numerator,ExactSum):
            self.a = numerator
        self.b = denominator
        self.constB = constB
    def simplify(self):
        if not self.exact: return
        for i in range(2,min(self.a,self.b)+1):
            if self.a%i == 0 and self.b%i == 0:
                self.a = self.a//i
                self.b = self.b//i
        for i in range(len(self.constA)):
            while self.constA[i] > 0 and self.constB[i] > 0:
                self.constA[i]-=1; self.constB[i]-=1 
    def ToString(self):
        if self.exact:
            self.constStrA = ""
            self.constStrB = ""
            for i,j in enumerate(self.constA):
                if j == 1:
                    self.constStrA += cnst.CONSTANTS[i][2]
                elif j > 1: self.constStrA += "{0}^{1}".format(cnst.CONSTANTS[i][2],j)   
            for i,j in enumerate(self.constB):
                if j == 1:
                    self.constStrB += cnst.CONSTANTS[i][2]
                elif j > 1: self.constStrB += "{0}^{1}".format(cnst.CONSTANTS[i][2],j)
            if self.b == 1 and self.constStrB == "":
                return "{0}{1}".format("" if self.a == 1 and self.constStrA != "" else self.a, self.constStrB)
            else:
                return "{0}{1}\n--\n{2}{3}".format("" if self.a == 1 and self.constStrA != "" else self.a,self.constStrA,self.b,self.constStrB)
        else:
            return str(self.ToFloat())
    def ToFloat(self):
        acc = float(self.a / self.b)
        for i,j in enumerate(constA): acc *= (cnst.CONSTANTS[i][1] ** j)
        for i,j in enumerate(constB): acc /= (cnst.CONSTANTS[i][1] ** j)
        return acc
    def add(num1,num2):
        numSum = num()
        numSum.b = num1.b * num2.b
        numSum.a = num1.a*num2.b + num2.a*num1.b
        numSum.simplify()
        return numSum
        diff = [a-b for a,b in zip(num1.constB,num2.constA)]
        if all(a >= 0 for a in diff) or all(a <= 0 for a in diff):
            # acceptable denominators, return an exact value

        numSum.constB = [a+b for a,b in zip(num1.constB,num2.constB)]

    def sub(num1,num2):
        minusNum2 = num(-num2.a,num2.b,num2.constA,num2.constB)
        return num.add(num1,minusNum2)
    def mult(num1,num2):
        numMult = num()
        numMult.a = num1.a * num2.a
        numMult.b = num1.b * num2.b
        numMult.constA = [a+b for a,b in zip(num1.constA,num2.constA)]
        numMult.constB = [a+b for a,b in zip(num1.constB,num2.constB)]
        numMult.simplify()
        return numMult
    def div(num1,num2):
        if num2.a == 0:
            raise DivisionByZeroError
        invNum2 = num(num2.b,num2.a,num2.constB,num2.constA)
        return num.mult(num1,invNum2)

a = num(5,10,[2,0],[0,1])
b = num(1,3,[0,0],[1,0])
print(num.add(a,b).ToString())