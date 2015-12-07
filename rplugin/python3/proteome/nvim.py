from pathlib import Path

import neovim  # type: ignore

import trypnv
from trypnv import Log


class NvimFacade(trypnv.nvim.NvimFacade):

    def __init__(self, nvim: neovim.Nvim) -> None:
        super(NvimFacade, self).__init__(nvim, 'proteome')

    def switch_root(self, path: Path):
        self.vim.command('cd {}'.format(path))
        self.pautocmd('SwitchedRoot')
        Log.info('switched root to {}'.format(path))
        self.set_pvar('root', path)


__all__ = ['NvimFacade']
