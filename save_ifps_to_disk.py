import json, os

def save_ifps_to_disk(ifps):
    os.makedirs('glimt/ifp', exist_ok=True)
    id_to_ifp = {}
    for ifp in ifps:
        id = ifp['id']
        id_to_ifp[id] = ifp
        fn = f'glimt/ifp/{id}.json'
        with open(fn, 'w') as f:
            json.dump(ifp, f, indent=4)
    return id_to_ifp