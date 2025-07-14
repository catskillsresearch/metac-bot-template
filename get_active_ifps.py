from list_all_ifps import list_all_ifps
import pandas as pd
pd.set_option('display.max_colwidth', None)

def get_active_ifps():
    L = list_all_ifps()
    ifps = [ifp for ifp in L if ifp['state'] == 'active']
    id_to_ifp = {ifp['id']: ifp for ifp in ifps}
    alignment = [(ifp['id'], ifp['props']['title']) for ifp in ifps]
    df = pd.DataFrame(alignment, columns = ['id', 'title']).sort_values(by='id')
    return df, ifps, id_to_ifp