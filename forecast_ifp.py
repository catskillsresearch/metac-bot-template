from detailed_proposition import detailed_proposition
from wiki_semantic_search import wiki_semantic_search
from split_news_into_text_and_urls import split_news_into_text_and_urls
from create_source_summaries import create_source_summaries
from rephrase_binary_outcomes import rephrase_binary_outcomes
from format_research import format_research
from glimt_forecast_prompt import glimt_forecast_prompt
from humor_me import humor_me
from get_forecast_components import *
from median_forecast import median_forecast
from median_rationale import median_rationale
from jsx_request import jsx_request
from jsx_forecast import jsx_forecast
from datetime import datetime

def forecast_ifp(ifp, news):
    print('begin FORECASTING', ifp['id'], ifp['props']['title'], datetime.now())
    title_plus_criteria = detailed_proposition(ifp)
    wiki_articles = wiki_semantic_search(title_plus_criteria)
    ifp_news_sources, ifp_news_text = split_news_into_text_and_urls(ifp, news)
    source_summaries, sources = create_source_summaries(ifp['id'], title_plus_criteria, wiki_articles, ifp_news_sources, ifp_news_text)
    rephrase_binary_outcomes(ifp)
    research = format_research(source_summaries)
    prompt, rejected = glimt_forecast_prompt(ifp, research)

    ## Run the prompt 5 times
    prompt_tries = 2 # Waste of time on Mistral 4 bit
    answers = [humor_me(prompt, i+1) for i in range(prompt_tries)]
    binProbs = [get_bin_probs(a) for a in answers]
    rights = [get_rights(a) for a in answers]
    wrongs = [get_wrongs(a) for a in answers]
    
    ## Median forecasts and rationales
    forecast = rejected + median_forecast(binProbs)
    
    right = median_rationale(rights)
    wrong = median_rationale(wrongs)
    jsx_request(jsx_forecast(ifp['id'],forecast,right,wrong,sources))
    print('end FORECASTING', ifp['id'], ifp['props']['title'], datetime.now())