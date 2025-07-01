from RAGForecaster import RAGForecaster
from EnhancedResearchPro import EnhancedResearchPro
from load_research import load_research
from pull_asknews import pull_asknews

def gather_research(df, live, model):
    rag = RAGForecaster()
    research_bot = EnhancedResearchPro(rag, model)
    research_bot.process_dataframe(df, use_cutoff=False)
    rag.research_bot = research_bot
    df['research'] = df.apply(load_research, axis=1)
    df['asknews'] = df.apply(lambda x: pull_asknews(x, live), axis=1)
    # Updated learning field with raw text extraction
    df['learning'] = df.apply(
        lambda row: [
            m['raw_text'] 
            for m, _ in research_bot.retrieval_cache.get(row['title'], []) 
            if 'raw_text' in m  # Safety check for legacy entries
        ], 
        axis=1
    )
    df['context_fresh'] = df['learning'].apply(lambda x: len(x) > 0)
    return df, rag

if __name__=="__main__":
    import pandas as pd
    from load_secrets import load_secrets
    load_secrets()
    df = pd.read_json('debug.json')
    df1, rag = gather_research(df, True, 'gemma3:latest')
    print(df1)