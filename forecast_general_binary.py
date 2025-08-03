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
from datetime import datetime
from make_glimt_question import make_glimt_question
from save_ifps_to_disk import save_ifps_to_disk
from post_forecast import post_forecast
from detailed_proposition import detailed_proposition
from gather_news_for_ifps import gather_news_for_ifps
import os, json
from types import SimpleNamespace
from format_rationale import format_rationale
from forecast_fn import forecast_fn

def forecast_general_binary(ifp):
    fn = forecast_fn(ifp)
    ifp['question_type'] = 'binary'
    if os.path.exists(fn):
        print('already forecast:', ifp['id'], ifp['title'])
        with open(fn, 'r') as f:
            (forecast, right, wrong, sources) = json.load(f)
            ifp['prediction'] = forecast[0]
            ifp['forecast'] = format_rationale(right, wrong, sources)
        return
    row = SimpleNamespace(**{'conid': ifp['id'],
            'lastTradeDate': ifp['period'][-1].replace('-',''),
            'longDescription': ifp['title'],
            'shortDescription': ''})
    glp = make_glimt_question(row)
    glp['props']['details'] = ''
    id_to_ifp = save_ifps_to_disk([glp])
    news = gather_news_for_ifps([glp])
    title_plus_criteria = detailed_proposition(glp)
    wiki_articles = wiki_semantic_search(title_plus_criteria)
    glp_news_sources, glp_news_text = split_news_into_text_and_urls(glp, news)
    source_summaries, sources = create_source_summaries(glp['id'], title_plus_criteria, wiki_articles, glp_news_sources, glp_news_text)
    source_summaries = [x if 'Error ' not in x else '' for x in source_summaries ]
    rephrase_binary_outcomes(glp)
    research = format_research(source_summaries)
    prompt, rejected = glimt_forecast_prompt(glp, research)
    prompt_tries = 2 # Waste of time on Mistral 4 bit
    answers = [humor_me(prompt, i+1) for i in range(prompt_tries)]
    binProbs = [get_bin_probs(a) for a in answers]
    rights = [get_rights(a) for a in answers]
    wrongs = [get_wrongs(a) for a in answers]
    ## Median forecasts and rationales
    forecast = rejected + median_forecast(binProbs)
    right = median_rationale(rights)
    wrong = median_rationale(wrongs)
    result = (forecast, right, wrong, sources)
    with open(fn, 'w') as f:
        json.dump(result, f)
    rationale = format_rationale(right, wrong, sources)
    yes_probability = forecast[0]
    ifp['prediction'] = yes_probability
    ifp['forecast'] = rationale
    brow = SimpleNamespace(**{
        'id_of_question': ifp['id'],
        'id_of_post': ifp['group']['id'],
        'question_type': 'binary',
        'prediction': yes_probability,
        'forecast': rationale})
    post_forecast(brow)
    