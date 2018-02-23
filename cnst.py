CONSTANTS = [
    ['tau', 6.28318530717958623200, 'τ'],
    ['e',   2.71828182845904509080, 'e']
]

def replace_constants(string):
    for cnst in CONSTANTS:
        string = string.replace(cnst[0],str("{:.20f}".format(cnst[1])))
    return string