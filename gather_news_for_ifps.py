import os
from call_asknews import call_asknews

def gather_news_for_ifp(ifp):
    id, title, details = ifp['id'], ifp['props']['title'], ifp['props']['details']
    fn = f'glimt/news/{id}.txt'
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            return f.read()
    prompt = f"""{title}\n{details}"""
    news = call_asknews(prompt)
    with open(fn, 'w') as f:
        f.write(news)
    print('saved', fn)
    return news

def gather_news_for_ifps(ifps):
    os.makedirs('glimt/news', exist_ok=True)
    news = {ifp['id']: gather_news_for_ifp(ifp) for ifp in ifps}
    return news