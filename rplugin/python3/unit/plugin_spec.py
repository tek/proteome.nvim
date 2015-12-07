import sure  # NOQA
from flexmock import flexmock  # NOQA

import neovim  # type: ignore
from neovim.msgpack_rpc.event_loop.asyncio import AsyncioEventLoop
from neovim.msgpack_rpc.msgpack_stream import MsgpackStream
from neovim.msgpack_rpc.session import Session
from neovim.msgpack_rpc.async_session import AsyncSession

from proteome import Proteome, List

from unit._support.loader import _LoaderSpec

from tek.test import temp_dir  # type: ignore


def start_nvim():
    loop = AsyncioEventLoop('child', ['/bin/env', 'nvim', '--headless',
                                      '--embed'])
    msgpack_stream = MsgpackStream(loop)
    async_session = AsyncSession(msgpack_stream)
    session = Session(async_session)
    return neovim.Nvim.from_session(session)


class Proteome_(_LoaderSpec, ):

    def setup(self, *a, **kw):
        super(Proteome_, self).setup(*a, **kw)

    def add_project(self):
        p = Proteome()
        d = temp_dir('project1')
        data = List('some', d)
        p._add_root(data)
        p.projects.projects.should.have.length_of(1)
        pro = list(p.projects.projects.values())[0]
        pro.name.should.equal(data[0])


class ProteomePlugin_(_LoaderSpec):

    def setup(self):
        self.vim = start_nvim()

    def foo(self):
        self.vim.command('let foo = 1')

__all__ = ['Proteome_', 'ProteomePlugin_']
