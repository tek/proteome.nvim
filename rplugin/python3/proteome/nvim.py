import neovim  # type: ignore

import trypnv


class NvimFacade(trypnv.NvimFacade):

    def __init__(self, vim: neovim.Nvim) -> None:
        super(NvimFacade, self).__init__(vim, 'proteome')

__all__ = ['NvimFacade']
