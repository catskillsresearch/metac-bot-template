from extract_python import extract_python
from humor_me import humor_me

def get_underlying_urls_of_ifp(results, ifp):
    if ifp['post_id'] in results:
        return
    group = ifp['group']
    group_title = group['title']
    group_description = group['group_of_questions']['description']
    group_resolution_criteria = group['group_of_questions']['resolution_criteria']
    group_fine_print = group['group_of_questions']['fine_print']
    prompt = f"""
What are the financial underlyings referred to here: 

```question
{group_title}
{group_description}
{group_resolution_criteria}
{group_fine_print}
```
Output the URLs of the data sources, wrapped in a Python list, so like this

```python
[URL1, URL2]
```."""
    answer = eval(extract_python(humor_me(prompt)))
    results[ifp['post_id']] = (group_title, answer)
    
def get_underlying_urls(ifps):
    results = {}
    for ifp in ifps:
        get_underlying_urls_of_ifp(results, ifp)
    return results