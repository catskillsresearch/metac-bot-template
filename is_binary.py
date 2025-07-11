from outcomes import outcomes

def is_binary(ifp):
    return outcomes(ifp) == ['Yes', 'No']