from pathlib import Path  # type: ignore
from functools import reduce  # type: ignore
import importlib

import neovim  # type: ignore

from tryp import List, may

from trypnv import command, NvimStatePlugin, Log, msg_command

from proteome.nvim import NvimFacade
from proteome.env import Env
from proteome.state import ProteomeState
from proteome.plugins.core import (AddByName, Show, Create, SwitchRoot, Next,
                                   Prev)
from proteome.project import Projects


class Proteome(ProteomeState):

    def __init__(
            self,
            vim: NvimFacade,
            config_path: Path,
            plugins: List[str],
            bases: List[Path]
    ) -> None:
        self._config_path = config_path
        self._bases = bases
        core = 'proteome.plugins.core'
        super(Proteome, self).__init__(vim)
        self.plugins = (plugins + [core]).flat_map(self.start_plugin)

    @may
    def start_plugin(self, name: str):
        try:
            mod = importlib.import_module(name)
        except ImportError as e:
            msg = 'invalid proteome plugin module "{}": {}'.format(name, e)
            Log.error(msg)
        else:
            if hasattr(mod, 'Plugin'):
                return getattr(mod, 'Plugin')(self.vim)

    def init(self):
        return Env(
            config_path=self._config_path,
            bases=self._bases,
            projects=Projects()
        )

    @property
    def projects(self):
        return self.env.projects

    @may
    def unhandled(self, env, msg):
        return reduce(lambda e, plug: plug.process(e, msg), self.plugins, env)


@neovim.plugin
class ProteomePlugin(NvimStatePlugin):

    def __init__(self, vim: neovim.Nvim) -> None:
        super(ProteomePlugin, self).__init__(NvimFacade(vim))
        self.pro = None  # type: Proteome

    def state(self):
        return self.pro

    @neovim.command('ProteomeReload', nargs=0)
    def proteome_reload(self):
        self.proteome_quit()
        self.proteome_start()

    @command()
    def proteome_quit(self):
        if self.pro is not None:
            self.vim.clean()
            self.pro = None

    @command()
    def proteome_start(self):
        config_path = self.vim.ps('config_path')\
            .get_or_else('/dev/null')
        bases = self.vim.pl('base_dirs')\
            .get_or_else(List())
        plugins = self.vim.pl('plugins') | List()
        self.pro = Proteome(self.vim, Path(config_path), plugins, bases)
        self.vim.vim.call('ptplugin#runtime_after')

    @msg_command(Create)
    def pro_create(self):
        pass

    @msg_command(AddByName)
    def pro_add(self, name: str):
        self.pro.send(AddByName(name))

    @msg_command(Show, sync=True)
    def pro_show(self):
        pass

    @command()
    def pro_ctags(self, *names):
        pass

    @msg_command(SwitchRoot)
    def pro_to(self):
        pass

    @msg_command(Next)
    def pro_next(self):
        pass

    @msg_command(Prev)
    def pro_prev(self):
        pass

__all__ = ['ProteomePlugin', 'Proteome']
