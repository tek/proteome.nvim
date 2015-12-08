import sure  # NOQA
from flexmock import flexmock  # NOQA

import neovim  # type: ignore
from neovim.msgpack_rpc.event_loop.asyncio import AsyncioEventLoop
from neovim.msgpack_rpc.msgpack_stream import MsgpackStream
from neovim.msgpack_rpc.session import Session
from neovim.msgpack_rpc.async_session import AsyncSession

from unit._support.loader import _LoaderSpec


def _start_nvim():
    loop = AsyncioEventLoop('child', ['/bin/env', 'nvim', '--headless',
                                      '--embed'])
    msgpack_stream = MsgpackStream(loop)
    async_session = AsyncSession(msgpack_stream)
    session = Session(async_session)
    return neovim.Nvim.from_session(session)


class ProteomePlugin_(_LoaderSpec):

    def setup(self):
        self.vim = _start_nvim()

    def _foo(self):
        self.vim.command('let foo = 1')

__all__ = ['ProteomePlugin_']
