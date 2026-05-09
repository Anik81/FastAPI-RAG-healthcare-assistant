from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Language = Literal["en", "ja"]


class IngestResponse(BaseModel):
    id: str
    language: Language
    num_chunks: int
    source: str


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = 3


class DocSearchResult(BaseModel):
    id: str
    text: str
    score: float
    language: str
    source: str


class RetrieveResponse(BaseModel):
    query_language: Language
    results: List[DocSearchResult]


class GenerateRequest(BaseModel):
    query: str = Field(..., min_length=1)
    output_language: Optional[Language] = None


class GenerateResponse(BaseModel):
    query_language: Language
    output_language: Language
    answer: str
    sources: List[dict]