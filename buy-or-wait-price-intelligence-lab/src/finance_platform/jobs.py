from __future__ import annotations

from typing import Any, Awaitable, Callable, Protocol


class JobRunner(Protocol):
    async def enqueue(self, name: str, job: Callable[..., Awaitable[Any]], **kwargs: Any) -> str: ...


class InlineJobRunner:
    async def enqueue(self, name: str, job: Callable[..., Awaitable[Any]], **kwargs: Any) -> str:
        await job(**kwargs)
        return f"inline:{name}"
