import pandas as pd
import numpy as np

def vector_search(query, model, index, num_results=10):
    vector = model.encode(list(query))
    D, I = index.search(np.array(vector).astype("float32"), k=num_results)
    return D, I

def get_keywords(model, data, index, kw, num=10):
    # Load data and models
    D, I = vector_search([kw], model, index, num_results=num)
    set_kw_ids = set(data.id)
    

    kw_tar = list()
    member_id = list()
    id_type = list()

    # print(data)

    for id_ in I.flatten().tolist():
            if id_ in set_kw_ids:
                f = data[(data.id == id_)]
            else:
                continue
            kw_tar.append(f.keyword.values[0])
            member_id.append(f.memberID.values[0])
            id_type.append(f.memberID_type.values[0])

    
    df = pd.DataFrame({'kw': kw_tar, 'memid': member_id, 'idtype': id_type})
    df.memid = df.memid.astype(str)
    df.idtype = df.idtype.astype(str)

    return list(df['kw']), list(df['memid']), list(df['idtype'])

def flatten_str_list(memid):
    return_list = list()
    for ids in memid:
        for idsplit in ids.split(','):
            return_list.append(idsplit)
    return return_list