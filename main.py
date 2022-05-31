# fastapi
from fastapi import FastAPI, Response
import os
from bson import json_util
import traceback

# utils import
from database.database import load_researchers
from dataset.dataset import *
from api.model import *
from api.get_institution import get_institution_data

app = FastAPI()

error_response = {'message': '''Something went wrong''', 'code': 401 }

# load data, models, collections
try:
    en_data = load_en_data()
    en_faiss = load_en_faiss()
    en_model = load_en_model()
    researchers_collection = load_researchers()
except:
    print("Something went wrong")
    traceback.print_exc()
    quit()

@app.get("/")
async def ping():
    return "Hello kakenhi ML"

@app.post("/get-institution")
async def get_institution(req: KeywordQuery):
    global en_model
    global en_data
    global en_faiss
    try:
        resp_data = get_institution_data(en_model, en_data, en_faiss, researchers_collection, req)
        return resp_data
    except:
        traceback.print_exc()
        return error_response