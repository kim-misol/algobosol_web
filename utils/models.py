from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class AnalysisBase(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD")
    name: str
    buy_price: Optional[float] = None
    invest_points: List[str] = Field(default_factory=list)
    html: str = ""
    pdf_path: Optional[str] = None
    qty: Optional[float] = None
    sold: bool = False

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisUpdate(AnalysisBase):
    id: int

class AnalysisRead(AnalysisBase):
    id: int
