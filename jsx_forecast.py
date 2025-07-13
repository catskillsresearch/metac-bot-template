def jsx_forecast(id: int, 
                 probas: list[float],
                 reason: str,
                 wwcym: str,
                 urls: list[str]):

    """Format forecast upload with all the goodies"""
    
    reason = reason[0:1200] # hard size on GUI
    wwcym = wwcym[0:1200] # hard size on GUI
    U = repr([{"value": url, "index":i+1,"order":i+1} for i, url in enumerate(urls)]).replace("'", '"')
    return f"""[["ifps","submitFcst",{{"ifpId":{id},"data":{{"probas": {probas} }},"rationale":{{"type":"reason","reason":"{reason}","wwcym":"{wwcym}","urls":{U}}},"publish":true}}]]"""
