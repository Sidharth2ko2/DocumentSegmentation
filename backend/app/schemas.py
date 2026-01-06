from pydantic import BaseModel
from typing import List


class DocResponse(BaseModel):
    name: str
    label: str
    confidence: float


class SearchResponse(BaseModel):
    results: List[str]