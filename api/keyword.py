import pandas as pd
import numpy as np
import numpy.linalg as LA

def vector_search(query, model, index, num_results: int = 10):
    vector = model.encode(list(query))
    D, I = index.search(np.array(vector).astype("float32"), k=num_results)
    return D, I

def get_keywords(model, data, index, kw, num: int = 10):
    # Load data and models
    D, I = vector_search(list(kw), model, index, num_results=num)
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
            kw_tar.append(str(f.keyword.values[0]))
            member_id.append(str(f.memberID.values[0]))
            id_type.append(str(f.memberID_type.values[0]))

    
    df = pd.DataFrame({'kw': kw_tar, 'memid': member_id, 'idtype': id_type})
    return list(df['kw']), list(df['memid']), list(df['idtype'])

def cos_angle(a, b):
    '''calculate similarity between two given vectors
    Parameter:
    ---------
        a : N dimentional vector (list of N integers)
        b : N dimentional vector
    
    Returns
    -------
        float cosine of angle between the given vectors (a and b)
    '''

    inner = np.inner(a, b)
    norms = LA.norm(a) * LA.norm(b)
    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    sim = np.cos(rad)
    return sim

def get_key_sim(model, data, index, user_query: str, threshold : float, num: int):
    '''Get graph related data for a given user query
    Parameters
    ----------
        model : the model which takes in a string and returns it's vector embedding
        data : the data that coresponds to the ids passed to the faiss index
        index : the faiss index object
        user_query : string to be looked up for
        num : number of keywords to be looked up for
        threshold : the level of similarity requrired (default is 0.5)
    
    Returns
    -------
        a dictionary containing graph data as the source, target and similarity and the map of keywords to member ids as keywords-memberIDs 
    '''
    resdf, memid, idtype = get_keywords(model, data, index , user_query, num)
    #Create a matrix
    embeddings = model.encode(resdf, show_progress_bar=True)

    src = list()
    tar = list()
    sim = list()
    thresh = threshold
    n = len(embeddings)
    m=0
    for i in range(n):
        m+=1
        for j in range(m):
            _sim = cos_angle(embeddings[i], embeddings[j])
            if i == j or _sim < thresh: continue
            src.append(resdf[i])
            tar.append(resdf[j])
            sim.append(float(_sim))
    return dict({
        "similarity": sim[:num],
        "memberid": memid[:num]
    })

def flatten_str_list(memid):
    return_list = list()
    for ids in memid:
        for idsplit in ids.split(','):
            return_list.append(idsplit)
    return return_list