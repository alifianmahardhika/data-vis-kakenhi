from pydantic import BaseModel

class KeywordQuery(BaseModel):
    keywords: str = ''
    threshold: float = 0.1
    resultnum: int = 50