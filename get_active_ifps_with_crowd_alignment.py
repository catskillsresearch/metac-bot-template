from get_active_ifps import get_active_ifps
import numpy as np
import pandas as pd

def get_active_ifps_with_crowd_alignment():
    _, ifps, id_to_ifp = get_active_ifps()
    alignment = [(ifp['id'], ifp['props']['title'], np.linalg.norm(np.array(ifp['myFcst']['probas'])-np.array(ifp['crowdFcst']['probas']))) for ifp in ifps]
    df = pd.DataFrame(alignment, columns = ['id', 'title', 'distance']).sort_values(by='distance')
    return df, ifps, id_to_ifp