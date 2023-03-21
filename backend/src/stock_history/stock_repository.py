from abc import ABC
from typing import List, Optional

import pandas as pd
import yahooquery as yf
from src.company.company_repository import company_repository
from src.exceptions import TickerNotFoundException
from src.models.model import CompanyStockHistory, TimeSeries
from src.models.time_range import Period
from src.stock_history.dao.stock_dao import CompanyStockHistoryDAO

__all__ = ("ts_repository",)


class YFinanceStockHistoryRepository(CompanyStockHistoryDAO, ABC):
    async def get_history_by_ticker_and_period(
        self, ticker: str, period: Period = Period.one_month
    ) -> Optional[CompanyStockHistory]:
        ticker_info = yf.Ticker(
            ticker,
            asynchronous=True,
            backoff_factor=0.2,
            retry=5,
            max_workers=4,
        )
        df_history = ticker_info.history(
            period=period.value, interval=period.interval.value
        )
        time_series = self._get_timeseries_data(df_history)
        if len(time_series) == 0:
            raise TickerNotFoundException()
        delta, delta_percentage = None, None
        if len(time_series) >= 2:
            delta = time_series[-1].value / time_series[-2].value
            delta_percentage = delta - 1
        return CompanyStockHistory(
            symbol=ticker,
            delta=delta,
            delta_percentage=delta_percentage,
            history=time_series,
        )

    async def search_company_history(
        self, query, period: Period = Period.one_month
    ) -> Optional[CompanyStockHistory]:
        company = await company_repository.search(query)
        if company is None:
            return
        company_history = await self.get_history_by_ticker_and_period(
            company.symbol, period
        )
        company_history.company_name = company.shortname
        return company_history

    @staticmethod
    def _get_timeseries_data(df: pd.DataFrame) -> List[TimeSeries]:
        if df.shape[0] > 0:
            df_process = df.reset_index()[["close", "date"]]
            df_process["date"] = pd.to_datetime(df_process["date"])
            records = df_process.to_dict("records")
            if len(records) > 0:
                print(records[0]["date"])
                return [
                    TimeSeries(timestamp=record["date"], value=record["close"])
                    for record in records
                ]
        return []


ts_repository = YFinanceStockHistoryRepository()
