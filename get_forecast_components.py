def get_bin_probs(r):
    return eval(r.split('```binProbs')[1].split('```')[0].strip())

def get_rights(r):
    return r.split('```rRight')[1].split('```')[0].strip()

def get_wrongs(r):
    return r.split('```rWrong')[1].split('```')[0].strip()