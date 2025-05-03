from forecasting_tools import MetaculusApi, ApiFilter
import asyncio

def get_resolved_questions(tournament_id):
    resolved_questions = []
    offset = 0
    batch_size = 100
    while True:
        api_filter = ApiFilter(
                    allowed_tournaments=[tournament_id],
                    allowed_statuses=["resolved"],
                    limit=batch_size,
                    offset=offset
                )
        batch = asyncio.run(MetaculusApi.get_questions_matching_filter(api_filter))
        if not batch:
            break
        resolved_questions.extend(batch)
        if len(batch) < batch_size:
            break
        offset += batch_size
        if offset > 300:
            break
        print("offset", offset)
    
    return resolved_questions

if __name__=="__main__":

    from load_secrets import load_secrets
    load_secrets()
    
    ## Retrieve all old resolved questions
    tourneys=[MetaculusApi.AI_COMPETITION_ID_Q3, 
              MetaculusApi.AI_COMPETITION_ID_Q4, 
              MetaculusApi.AI_COMPETITION_ID_Q1, 
              MetaculusApi.AI_COMPETITION_ID_Q2]   
    questions = []
    for tournament_id in tourneys:
        print(tournament_id)
        resolved_questions = get_resolved_questions(tournament_id)
        questions.extend(resolved_questions)
    print("retrieved", len(questions))

    from pickle_objects import *
    qfn = 'all_questions.pkl'
    pickle_objects(questions, qfn)
    q2 = unpickle_objects(qfn)
    print("saved", len(q2))
