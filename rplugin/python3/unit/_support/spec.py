from flexmock import flexmock  # type: ignore

import tek  # type: ignore

import trypnv

from proteome.nvim import NvimFacade


class Spec(tek.Spec):

    def setup(self, *a, **kw):
        trypnv.development = True
        super(Spec, self).setup(*a, **kw)


class MockNvimSpec(Spec):

    def setup(self, *a, **kw):
        super(MockNvimSpec, self).setup(*a, **kw)
        self.vim = NvimFacade(None)
        self.vim_mock = flexmock(self.vim)

__all__ = ['Spec']
