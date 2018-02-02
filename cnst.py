import math
CONSTANTS = [
    ['tau',2*math.pi],
    ['e',math.e],
]

def replace_constants(string):
    for cnst in CONSTANTS:
        string = string.replace(cnst[0],str(cnst[1]))
    return string