from typing import Optional
from pydantic import BaseModel

class KeywordQuery(BaseModel):
    keywords: Optional[str] = ''
    resultnum: Optional[int] = 100