# fastapi
import traceback
from fastapi import FastAPI
from utils import mockup_data
# utils import
from api.model import *

app = FastAPI()

error_response = {'message': '''Something went wrong''', 'code': 401 }

# load data, models, collections

@app.get("/")
async def ping():
    return "Hello kakenhi ML"

@app.post("/get-institution")
async def get_nodes_keyword(req: KeywordQuery):
    try:
        print("/get-institution", req)
        return_data = mockup_data.data()
        return {"data": return_data}
    except:
        traceback.print_exc()
        return error_response