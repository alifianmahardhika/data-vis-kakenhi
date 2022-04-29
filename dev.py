# fastapi
import traceback
from fastapi import FastAPI

# utils import
from api.model import *

app = FastAPI()

error_response = {'message': '''Something went wrong''', 'code': 401 }

# load data, models, collections

@app.get("/ping")
async def ping():
    return "Hello kakenhi ML"

@app.post("/get-institution")
async def get_nodes_keyword(req: KeywordQuery):
    try:
        print("/get-institution", req)
        return_data = list()
        example_name = ['Alifian', 'Saadullah', 'Satria']
        example_institution = ['Kobe-U', 'Tokyo-U', 'Kanazawa-U']
        example_id = ["10633472", "10855307", "10748198"]
        for inst in example_institution:
            researcher_profiles = list()
            print(inst)
            for profile_name in example_name:
                ob = {"firstName": profile_name, "kakenhiID": example_id[0]}
                researcher_profiles.append(ob)
        #     print({"institution": inst, "researcherProfiles": researcher_profiles})
            return_data.append({"institution": inst, "researcherProfiles": researcher_profiles})
        return {"data": return_data}
    except:
        traceback.print_exc()
        return error_response