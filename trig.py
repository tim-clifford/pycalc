import math, cnst
ACCURACY = 20
TOLERANCE = 0.002
TAU = cnst.CONSTANTS[0][1]
def fact(x):
	if x != int(x): raise ArithmeticError
	if x < 0: raise ArithmeticError
	if x == 0: return 1
	return x * fact(x-1)
def comb(n,r):
	return fact(n)/(fact(r)*fact(n-r))
def sin(x):
	if x < 0: return -sin(-x)
	x %= TAU
	acc = float(0)
	for i in range(ACCURACY):
		acc += (-1)**i * (x**(2*i - 1)/fact(2*i+1))
	return acc
def cos(x):
	if x < 0: return cos(-x)
	x %= TAU
	acc = float(0)
	for i in range(ACCURACY):
		acc += (-1)**i * (x**(2*i))/fact(2*i)
	return acc
def tan(x): 
	x %= TAU
	if abs(cos(x)) < TOLERANCE: raise ArithmeticError
	return sin(x)/cos(x)
def sec(x): 
	if abs(cos(x)) < TOLERANCE: raise ArithmeticError
	return 1/cos(x)
def csc(x): 
	if abs(sin(x)) < TOLERANCE: raise ArithmeticError
	return 1/sin(x)
def cot(x): 
	if abs(tan(x)) < TOLERANCE: raise ArithmeticError
	return 1/tan(x)
def arcsin(x):
	if abs(x) > 1: raise ArithmeticError
	acc = 0
	for n in range(ACCURACY):
		acc += (comb(2*n,n)*x**(2*n+1))/(4**n*(2*n+1))
	return acc
def arccos(x):
	return TAU/4 - arcsin(x)
def arctan(x):
	acc = 0
	for n in range(ACCURACY):
		acc += (-1)**n*(x**(2*n+1)/(2*n+1))
	if acc > TAU/2: return acc - TAU
	if acc < TAU/-2: return acc + TAU
	return acc
def abs(x):
	if x < 0: return -1*x
	else: return x
def test():
	assert abs(sin(3.14)-math.sin(3.14)) < TOLERANCE
	assert abs(cos(3.14)-math.cos(3.14)) < TOLERANCE
	assert abs(tan(3.14)-math.tan(3.14)) < TOLERANCE
	assert abs(arcsin(0.3)-math.asin(0.3)) < TOLERANCE
	assert abs(arccos(0.3)-math.acos(0.3)) < TOLERANCE
	assert abs(arctan(0.3)-math.atan(0.3)) < TOLERANCE
	#assert abs(sin(25)-math.sin(25)) < TOLERANCE
	try: 
		arcsin(3)
		raise AssertionError
	except ArithmeticError: pass
if __name__ == "__main__": print(sin(-1))