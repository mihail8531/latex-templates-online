from typing import Generic, Protocol, TypeVar

from repositories.repository import BaseRepository


class BaseService(Protocol):
    _repository: BaseRepository

    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository
