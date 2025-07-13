from humor_me import humor_me
import os, json
from is_binary import is_binary

def rephrase_binary_outcomes(ifp):
    if not is_binary(ifp):
        return
   
    fn = f'glimt/prompt/{ifp["id"]}/rephrase_binary_outcome.json'
    if not os.path.exists(fn):
        title = ifp['props']['title']
        
        prompt = f"""We ask the question
        ```question
        {title}
        ```
        
        This question has a Yes or No answer.  
        If Yes then an event has occurred.  
        If No then the event did not occur.
        
        Please TWO ITEMS, in this format:
        
        ```event_occurs
        A phrase you would say if the event will occur
        ```
        
        ```event_doesnt_occur
        A phrase you would say if the event will not occur
        ```
        
        Use backticks ```event_occurs to mark the first response and ```event_doesnt_occur to mark the second response.
        
        Use future tense "will" not past tense "has"."""
        
        phrases = humor_me(prompt)
        positive = phrases.split('```event_occurs')[1].split('```')[0].strip()
        negative = phrases.split('```event_doesnt_occur')[1].split('```')[0].strip()
        with open(fn, 'w') as f:
            json.dump({'Yes': positive, 'No': negative}, f, indent=4)
    else:
        with open(fn, 'r') as f:
            d = json.load(f)
            positive, negative = d['Yes'],d['No']
    
    ifp['bins'][0]['props']['title'] = positive
    ifp['bins'][1]['props']['title'] = negative