# fastapi
import traceback
from fastapi import FastAPI, Response
import os
from bson import json_util

# utils import
from database.database import load_researchers
from dataset.dataset import *
from api.model import *
from api.keyword import *

app = FastAPI()

error_response = {'message': '''Something went wrong''', 'code': 401 }

# load data, models, collections
try:
    en_data = load_en_data()
    en_faiss = load_en_faiss()
    en_model = load_en_model()
    researchers = load_researchers()
except:
    print("Something went wrong")
    traceback.print_exc()
    quit()

@app.get("/ping")
async def ping():
    return "Hello kakenhi ML"

@app.post("/get-institution")
async def get_nodes_keyword(req: KeywordQuery):
    global en_model
    global en_data
    global en_faiss
    from pandas import DataFrame

    try:
        print("/get-institution", req)
        keywords_list, id_list, id_type = get_keywords(en_model, en_data, en_faiss, req.keywords, 50)
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
        id_query = {"$or": [{ "researchmapID": { "$in": ids } }, { "kakenhiID": { "$in": ids } }]}
        pipeline = [
            {"$match": {
                "$and": [
                    id_query,
                ],
            }},
            select_field,
            {"$limit" :  200},
        ]
        print(pipeline)
        df = DataFrame(list(researchers.aggregate(pipeline)))
        return_data = list()
        for inst in list(df['institution'].unique()):
            researcher_profiles = list()
            filtered_df = df[df["institution"]==inst][['name', 'kakenhiID']]
            for idx in range(len(filtered_df)):
                profile_name = filtered_df.iloc[idx][0] # name
                kak_id = filtered_df.iloc[idx][1] # kakenhi ID
                ob = {"firstName": profile_name, "kakenhiID": kak_id}
                researcher_profiles.append(ob)
            print({"institution": inst, "researcherProfiles": researcher_profiles})
            return_data.append({"institution": inst, "researcherProfiles": researcher_profiles})
        return {"data": return_data}
    except:
        traceback.print_exc()
        return error_response