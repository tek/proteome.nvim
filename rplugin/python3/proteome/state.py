from typing import TypeVar, Generic

from trypnv.machine import Machine, StateMachine

from proteome.nvim import NvimFacade

A = TypeVar('A')


class ProteomeComponent(Generic[A], Machine[A]):

    def __init__(self, v: NvimFacade) -> None:
        self.vim = v


class ProteomeState(Generic[A], StateMachine[A]):

    def __init__(self, vim: NvimFacade) -> None:
        self.vim = vim
        super(ProteomeState, self).__init__()


__all__ = ['ProteomeComponent', 'ProteomeState']
