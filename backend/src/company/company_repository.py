from abc import ABC
from functools import lru_cache
from typing import Optional

import httpx

from src.company.dao.company_dao import CompanyDAO
from src.exceptions import NetworkErrorException, SearchNotFoundException
from src.config import get_logger
from src.models.model import Company

__all__ = ("company_repository",)

logger = get_logger()


class _CompanyHttpRepository(CompanyDAO, ABC):
    URL = "https://query2.finance.yahoo.com/v1/finance/search"
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    def __int__(self):
        pass

    async def _search_company(self, query):
        try:
            params = {"q": query, "quotes_count": 1, "country": "United States"}
            async with httpx.AsyncClient(http2=True) as client:
                result = await client.get(url=self.URL, params=params, headers={'User-Agent': self.USER_AGENT})
            return result
        except Exception as e:
            logger.error(e)
            raise NetworkErrorException()

    async def search(self, query: str) -> Optional[Company]:
        result = await self._search_company(query)
        if result.status_code == 200:
            data = result.json()
            if len(data["quotes"]) > 0:
                quote = data['quotes'][0]
                logger.info(f"Search result: {quote}")
                return Company(**quote)
            raise SearchNotFoundException()


company_repository = _CompanyHttpRepository()


class _CompanyMongoRepository(CompanyDAO, ABC):
    # TODO: implement here when you'd like to choice mongodb as a database storage
    async def search(self, query: str) -> Optional[Company]:
        pass


class _CompanyJDBCRepository(CompanyDAO, ABC):
    # TODO: implement here when you'd like to choice jdbc as a database storage
    async def search(self, query: str) -> Optional[Company]:
        pass
