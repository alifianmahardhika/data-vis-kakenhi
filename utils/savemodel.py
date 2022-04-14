import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

sentences = ["This is an example sentence", "Each sentence is converted"]
model_path = "models/keywords/jp"

if os.getenv("KEYWORD_ML_MODEL"):
    model_name = str(os.environ.get("KEYWORD_ML_MODEL"))

model = SentenceTransformer(model_name)
embeddings = model.encode(sentences)
print(embeddings)
model.save(model_path)