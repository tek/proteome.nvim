from typing import TypeVar, Generic

from trypnv.machine import Machine, StateMachine
from trypnv.cmd import StateCommand
from trypnv import Log

from proteome.nvim import NvimFacade

from fn import F, _  # type: ignore

from tek.tools import camelcaseify  # type: ignore

A = TypeVar('A')


class ProteomeComponent(Generic[A], Machine[A]):

    def __init__(self, name: str, v: NvimFacade) -> None:
        self.name = name
        self.vim = v

    def _command_by_message_name(self, name: str):
        msg_name = camelcaseify(name)
        return self._message_handlers\
            .find_key(lambda a: a.__name__ == msg_name)\

    def command(self, name: str, args: list):
        return self._command_by_message_name(name)\
            .map(lambda a: StateCommand(a[0]))\
            .cata(_.call('dispatch', self, args),
                  F(self._invalid_command, name))

    def _invalid_command(self, name):
        Log.error('plugin "{}" has no command "{}"'.format(self.name, name))
        return Empty()


class ProteomeState(Generic[A], StateMachine[A]):

    def __init__(self, vim: NvimFacade) -> None:
        self.vim = vim
        super(ProteomeState, self).__init__()


__all__ = ['ProteomeComponent', 'ProteomeState']
