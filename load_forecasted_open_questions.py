import glob, joblib, os

def load_forecasted_open_questions(num_questions, model):
    start, end = num_questions
    fns = glob.glob('open/*.joblib')
    fns = [(int(fn.split('/')[1].split('.')[0]), fn) for fn in fns]
    qdir = f'forecast_{model}'
    fns = [fn for id,fn in fns if start <= id <= end and 
           os.path.exists(fn.replace('open', qdir).replace('joblib', 'md'))]
    ids = sorted([int(fn.split('/')[1].split('.')[0]) for fn in fns])
    questions = [joblib.load(fn) for fn in fns]
    return questions

if __name__=="__main__":
    questions = load_forecasted_open_questions((0, 100000), 'llama3')
    for question in questions:
        print(type(question))

