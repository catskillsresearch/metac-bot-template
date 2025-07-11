from jsx_request import jsx_request
from days_from_0_to_datetime import days_from_0_to_datetime

def list_active_ifps():
    """## Query active IFPs
        To request the list of active IFPs, replace jsxRequest by:       
        [["ifps", "queryIFPs", {query: {states: ["active"]}, fmt: {}}]]
        
        It will return a JSON array of all active iFPs and their detailed properties, including:
        * **symbol**
        * **title**
        * **details**: Information beyond the title of the IFP, such as what sources may be used to resolve the IFP, and/or some background information that might be useful to forecasters, &c.
        * **bins**: An array of the proposed resolution outcomes
        """
    
    L = jsx_request("""[["ifps", "queryIFPs", {query: {states: ["active"]}, fmt: {}}]]""")
    ifps = L[0]
    for ifp in ifps:
        for key in ifp['dates']:
            value = ifp['dates'][key]
            ifp['dates'][key] = days_from_0_to_datetime(value)
    return ifps
