from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Any
from os.path import realpath


class Context(ABC):

    def __init__(
        self,
        base_directory: str,
        options: Namespace | None = None,
        plugins: list['Plugin'] | None = None
    ) -> None:
        self._base_directory: str = base_directory

    def base_directory(self, canonical_path: bool = True) -> str:
        return (
            self._base_directory
            if not canonical_path else
            realpath(self._base_directory)
        )

    def defaults(self) -> dict[str, Any]:
        return {}

    def dry_run(self) -> bool:
        return False


class Messenger():

    def debug(self, message: str) -> None:
        message = message.strip()

    def action(self, message: str) -> None:
        message = message.strip()

    def info(self, message: str) -> None:
        message = message.strip()

    def lowinfo(self, message: str) -> None:
        message = message.strip()
        self.info(message)

    def warning(self, message: str) -> None:
        message = message.strip()

    def error(self, message: str) -> None:
        message = message.strip()


class Plugin(ABC):

    supports_dry_run: bool = False

    def __init__(self, context: Context) -> None:
        self._context: Context = context
        self._log: Messenger = Messenger()

    @abstractmethod
    def can_handle(self, directive: str) -> bool:
        pass

    @abstractmethod
    def handle(self, directive: str, data: Any) -> bool:
        pass
