def detailed_proposition(ifp):
    return f"{ifp['props']['title']} {ifp['props']['details']}".replace('<p><b>', '').replace('</b><p>', '')
