# fastapi
import traceback
from fastapi import FastAPI, Response
import os
from bson import json_util

# utils import
from database.database import load_researchers
from dataset.dataset import *

app = FastAPI()

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
