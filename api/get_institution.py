from typing import List
from api.keyword import *
from api.model import *
from pandas import DataFrame, merge
from pymongo.collection import Collection

def assign_sim(id_list: List[str], sim_list: List[float]):
    # assign similarity to each ID
    tmp_list = list()
    tmp_similarity = list()
    for idx in range(len(id_list)):
        try:
            for ids in id_list[idx].split(','):
                tmp_list.append(ids)
                tmp_similarity.append(sim_list[idx])
        except:
            print("assign failed")
    id_sim_list = dict({"kakenhiID": tmp_list, "similarity": tmp_similarity})
    return id_sim_list

def get_institution_data(kw_model, kw_data, kw_faiss, researchers: Collection, req_data: KeywordQuery):
    ml_result = get_key_sim(kw_model, kw_data, kw_faiss, req_data.keywords, req_data.threshold, req_data.resultnum)
    sim_list = ml_result['similarity']
    id_list = ml_result['memberid']
    # assign similarity
    id_sim_list = assign_sim(id_list, sim_list)
    ids = list(set(flatten_str_list(id_list)))
    select_field = {
        "$project" :
        {
            "institution" : "$institutionName.en",
            "name" : "$name.en",
            "kakenhiID": "$kakenhiID",
            "_id" : 0
            }
    }
    id_query = {"kakenhiID": { "$in": ids } }
    pipeline = [
        {"$match": {
            "$and": [
                id_query,
            ],
        }},
        select_field,
        {"$limit" :  50},
    ]
    df_similarity = DataFrame.from_dict(id_sim_list)
    df_researcher = DataFrame(list(researchers.aggregate(pipeline)))
    df = merge(df_researcher, df_similarity, on='kakenhiID')
    return_data = list()
    for inst in list(df['institution'].unique()):
        researcher_profiles = list()
        # print(inst)
        filtered_df = df[df["institution"]==inst][['name', 'kakenhiID', 'similarity']]
        for idx in range(len(filtered_df)):
            profile_name = filtered_df.iloc[idx][0] # name
            kak_id = filtered_df.iloc[idx][1] # kakenhi ID
            sim = filtered_df.iloc[idx][2] # similarity score
            ob = {"firstName": str(profile_name), "kakenhiID": str(kak_id), "similarity": float(sim)}
            researcher_profiles.append(ob)
        # print({"institution": inst, "researcherProfiles": researcher_profiles})
        return_data.append({"institution": inst, "researcherProfiles": researcher_profiles})
    return {"data": return_data}