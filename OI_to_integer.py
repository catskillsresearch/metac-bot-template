def OI_to_integer(OI):
    if OI[-1] == 'K':
        return float(OI[:-1])*1000.0
    elif OI[-1] == 'M':
        return float(OI[:-1])*1000000.0
    else:
        return float(OI)