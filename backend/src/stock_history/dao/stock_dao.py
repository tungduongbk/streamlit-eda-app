from abc import ABC, abstractmethod
from typing import Optional

from models.model import CompanyStockHistory
from models.time_range import Period


class CompanyStockHistoryDAO(ABC):
    @abstractmethod
    async def get_history_by_ticker_and_period(
        self, ticker: str, period: Period
    ) -> Optional[CompanyStockHistory]:
        pass

    @abstractmethod
    async def search_company_history(
        self, query: str, period: Period = Period.one_month
    ) -> Optional[CompanyStockHistory]:
        pass

    # TODO: Implement query multiple tickers at once - for reduce round trip purpose
