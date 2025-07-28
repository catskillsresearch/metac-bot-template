from humor_me import humor_me
from tqdm import tqdm
import os, json

def create_source_summaries(ifp_id, title_plus_criteria, wiki_articles, ifp_news_sources, ifp_news_text):
    
    fn = f'glimt/source_summaries/{ifp_id}.json' # source summaries
    fn1 = f'glimt/source_summaries/{ifp_id}.txt'  # source URLs
    fn2 = f'glimt/source_summaries/{ifp['id']}_combined.txt' # source summaries
    
    if os.path.exists(fn) and os.path.exists(fn1):
        with open(fn, 'r') as f:
            source_summaries = json.load(f)
        with open(fn1, 'r') as f:
            sources = [x.strip() for x in f.readlines()]

        return source_summaries, sources

    combined = list(zip(ifp_news_sources, [x.replace('**', '') for x in ifp_news_text])) + [(z, z.text) for x,y,z in wiki_articles]
    source_summaries = []
    for item in tqdm(combined):
        content = item[1]
        prompt = f"""You are an expert intelligence analyst.
You are researching this question:
```title_plus_criteria
{title_plus_criteria}
```

You are given this content: 
```content
{content}
```

Create a new text which contains, in a form easily understood by you, 
information that you would want to consider when deciding the question."""
    
        summary = humor_me(prompt)
        source_summaries.append(summary)
    
    os.makedirs('glimt/source_summaries', exist_ok=True)
    
    with open(fn, 'w') as f:
        json.dump(source_summaries, f, indent=4)

    ifp_wiki_sources = [z.fullurl for x,y,z in wiki_articles]
    sources = ifp_news_sources + ifp_wiki_sources

    with open(fn2, 'w') as f:
        f.write('\n'.join(source_summaries))

    return source_summaries, sources