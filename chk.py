from main import BRACKETS,ops

#TODO: UPDATE FOR PREFIXES. THIS FUNCTION CURRENTLY NOT CALLED
def check(string):
    # using regular expression, with stripped brackets: ([0-9.]+[`operators`])*[0-9.]
    for i in "".join(["".join(a) for a in BRACKETS]): string = string.replace(i,"").replace(" ","")
    # couldn't get regex to work. Plus, no importing, right?
    index = 0
    # allow the '- not an operator' edge case
    if string[0] == '-' and len(string) > 1:
        string = string[1:]
    while True:
        try:
            if not string[index] in '0123456789.': 
                return False
            else: 
                while index < len(string) and string[index] in '0123456789.': 
                    index += 1
                if index == len(string): return True
            if not string[index] in "".join(ops):
                return False
            else: index = index + 1
        except IndexError:
            return False