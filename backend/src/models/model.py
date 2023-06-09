from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

__all__ = (
    "TimeSeries",
    "CompanyStockHistory",
    "Company",
)


def to_snake_case(string: str) -> str:
    return "".join(
        ["_" + i.lower() if i.isupper() else i for i in string]
    ).lstrip("_")


class TimeSeries(BaseModel):
    timestamp: datetime
    value: float

    def dict(self, include_nulls=False, **kwargs):
        kwargs["exclude_none"] = not include_nulls
        return super().dict(**kwargs)


class CompanyStockHistory(BaseModel):
    symbol: str
    company_name: Optional[str]
    history: List[TimeSeries]
    delta: Optional[float]
    delta_percentage: Optional[float]


class Company(BaseModel):
    symbol: str
    shortname: str
    industry: Optional[str]
    score: float

    class Config:
        alias_generator = to_snake_case
