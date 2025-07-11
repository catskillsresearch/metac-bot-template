def outcomes(ifp):
    return [x['props']['title'] for x in ifp['bins']]