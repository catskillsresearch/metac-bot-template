import os, json

def saved_prompt(ifp):
    os.makedirs('glimt/prompt', exist_ok=True)
    dlgdir = f'glimt/prompt/{ifp["id"]}'
    os.makedirs(dlgdir, exist_ok=True)
    fn = f'{dlgdir}/question.json'
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            return (fn, json.load(f))
    else:
        return (fn, None)
