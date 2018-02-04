import cnst
class num:
    exact = True
    a = 1
    b = 1
    constA = [0]*len(cnst.CONSTANTS)
    constB = [0]*len(cnst.CONSTANTS)
    def __init__(self,numerator,denominator,constA,constB):
        self.a = numerator
        self.b = denominator
        self.constA = constA
        self.constB = constB
    def simplify(self):
        for i in range(2,min(self.a,self.b)+1):
            if self.a%i == 0 and self.b%i == 0:
                self.a = self.a//i
                self.b = self.b//i
        for i in range(len(self.constA)):
            while self.constA[i] > 0 and self.constB[i] > 0:
                print("Yup")
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
            return "Not Implemented"
def add(num1,num2):
    numSum = num(1,1,[0]*len(cnst.CONSTANTS))
    numSum.b = num1.b * num2.b
    #numSum.constB = map(lambda a,b: a+b,num1.constB,num2.constB)
    #numSum.a = num1.a*

a = num(5,10,[2,1],[0,1])
a.simplify()
print(a.ToString())