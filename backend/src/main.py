import uvicorn
from config import api_settings
from exceptions import (
    SearchNotFoundException,
    TickerNotFoundException,
    get_exception_responses,
)
from fastapi import FastAPI
from middlewares import request_handler
from src.models.model import CompanyStockHistory
from src.models.time_range import Period
from stock_history.stock_repository import ts_repository

__all__ = ("app",)


app = FastAPI(title=api_settings.title)
app.middleware("http")(request_handler)


@app.get(
    "/stocks/history",
    response_model=CompanyStockHistory,
    description="Get stock stock_history",
    responses=get_exception_responses(TickerNotFoundException),
    tags=["stock"],
)
async def _get_history(ticker: str, period: Period = Period.one_month):
    company_history = await ts_repository.get_history_by_ticker_and_period(
        ticker, period
    )
    return company_history


@app.get(
    "/stocks/search",
    response_model=CompanyStockHistory,
    description="Get stock stock_history",
    responses=get_exception_responses(SearchNotFoundException),
    tags=["stock"],
)
async def _search_history(query: str, period: Period = Period.one_month):
    company_history = await ts_repository.search_company_history(query, period)
    return company_history


def run():
    uvicorn.run(
        app,
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
    )


if __name__ == "__main__":
    run()
