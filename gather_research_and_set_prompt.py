from RAGForecaster import RAGForecaster
from EnhancedResearchPro import EnhancedResearchPro
from load_research import load_research
from pull_asknews import pull_asknews
from prompt_question import prompt_question

def gather_research_and_set_prompt(df):
    rag = RAGForecaster()
    research_bot = EnhancedResearchPro(rag)
    research_bot.process_dataframe(df, use_cutoff = False)
    df['research'] = df.apply(load_research, axis=1)
    df['asknews'] = df.apply(pull_asknews, axis=1)
    df['learning'] =  df.apply(lambda row: research_bot.retrieval_cache.get(row['title'], ''), axis=1)
    df['prompt'] = df.apply(prompt_question, axis=1)  # takes in asknews and learning
    return df, rag
