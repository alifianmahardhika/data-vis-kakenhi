from typing import List, Optional
from pydantic import BaseModel

class KeywordQuery(BaseModel):
    keywords: Optional[str] = ''
    resultsNum: Optional[int] = 100