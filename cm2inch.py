def cm2inch(*centy):  # Converting centimeters to inches
    inch = 2.54
    if isinstance(centy[0], tuple):
        return tuple(i/inch for i in centy[0])
    else:
        return tuple(i/inch for i in centy)