import os

def saved_prompt(ifp):
    dlgdir = f'glimt/prompt/{ifp["id"]}'
    os.makedirs(dlgdir, exist_ok=True)
    fn = f'{dlgdir}/question.txt'
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            return (fn, f.read())
    else:
        return (fn, None)
