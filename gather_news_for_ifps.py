import os
from call_asknews import call_asknews

def gather_news_for_ifps(ifps):
    os.makedirs('glimt/news', exist_ok=True)
    news = {}
    for ifp in ifps:
        id, title, details = ifp['id'], ifp['props']['title'], ifp['props']['details']
        fn = f'glimt/news/{id}.txt'
        if os.path.exists(fn):
            with open(fn, 'r') as f:
                news[id] = f.read()
            continue
        prompt = f"""{title}\n{details}"""
        news[id] = call_asknews(prompt)
        with open(fn, 'w') as f:
            f.write(news[id])
        print('saved', fn)
    return news