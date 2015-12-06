import asyncio
from contextlib import contextmanager


@contextmanager
def test_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

__all__ = ['test_loop']
