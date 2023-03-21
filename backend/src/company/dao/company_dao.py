from abc import ABC, abstractmethod
from typing import Optional

from models.model import Company


class CompanyDAO(ABC):

    @abstractmethod
    async def search(self, query: str) -> Optional[Company]:
        pass
