from jsx_request import jsx_request
from days_from_0_to_datetime import days_from_0_to_datetime

def list_all_ifps():
    """## Query all IFPs
        
        It will return a JSON array of all active iFPs and their detailed properties, including:
        * **symbol**
        * **title**
        * **details**: Information beyond the title of the IFP, such as what sources may be used to resolve the IFP, and/or some background information that might be useful to forecasters, &c.
        * **bins**: An array of the proposed resolution outcomes
        """

    jsx = """[[
          "ifps",
          "queryIFPs",
          {
            "fmt": {
              "myFcst": true,
              "crowdFcst": true,
              "answer": true,
              "fcsterCnt": true,
              "ts": true
            }
          }
        ]]"""
    
    L = jsx_request(jsx)

    ifps = L[0]
    for ifp in ifps:
        for key in ifp['dates']:
            value = ifp['dates'][key]
            ifp['dates'][key] = days_from_0_to_datetime(value)
    return ifps