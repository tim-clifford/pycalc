import math
CONSTANTS = [
    ['tau',2*math.pi, 'τ'],
    ['e',math.e, 'e'],
]

def replace_constants(string):
    for cnst in CONSTANTS:
        string = string.replace(cnst[0],str("{:.20f}".format(cnst[1])))
    return string