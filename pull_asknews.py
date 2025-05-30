from call_asknews import call_asknews
import os

def pull_asknews(row, live):
    os.makedirs('asknews', exist_ok=True)
    fn = f'asknews/{row.id_of_question}.md'
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            return f.read()
    question = row.title
    news = call_asknews(question, live)
    with open(fn, 'w') as f:
        f.write(news)
    return news

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    class foo:
        def __init__(self, id, title):
            self.id_of_question = id
            self.title = title
            
    question = foo(999, "Will Elon Musk be the world's richest person on December 31, 2025?")
    news = pull_asknews(question. True)
    print(news)
    