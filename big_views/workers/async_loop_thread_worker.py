import asyncio
import threading
from typing import Any, Coroutine, Optional


class AsyncLoopThreadWorker:
    def __init__(self) -> None:
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._started = threading.Event()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def _runner() -> None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self._started.set()
            self.loop.run_forever()

        self._thread = threading.Thread(target=_runner, daemon=True)
        self._thread.start()
        self._started.wait()

    def stop(self) -> None:
        if not self.loop:
            return
        self.loop.call_soon_threadsafe(self.loop.stop)

    def run(self, coro: Coroutine[Any, Any, Any]) -> Any:
        if not self.loop:
            raise RuntimeError('Async loop not started')
        fut = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return fut.result()
