from pathlib import Path  # type: ignore

import neovim  # type: ignore

from tryp import Empty, List, Map

from trypnv import command, NvimPlugin

from proteome.project import Projects, Resolver, ProjectLoader, Project
from proteome.nvim import NvimFacade

from trypnv import Log


class Proteome(object):

    def __init__(
            self,
            vim: neovim.Nvim,
            config_path: Path,
            bases: List[Path]
    ) -> None:
        self.vim = vim
        self.projects = Projects()
        self._resolver = Resolver(bases, Map())
        self._loader = ProjectLoader(config_path, self._resolver)
        self._current_index = Empty()

    def add(self, pro: Project):
        self.projects = self.projects + pro

    def create(self, name: str, root: str):
        self.add(Project(name, Path(root)))

    def add_by_name(self, name: str):
        self._loader.by_name(name)\
            .foreach(self.add)

    def show(self, names: List[str]):
        lines = self.projects.show(names)
        header = List('Projects:')  # type: List[str]
        return '\n'.join(header + lines)

    def ctags(self, names: List[str]):
        pass

    def switch_root(self, name: str):
        self.projects.project(name)\
            .map(lambda a: a.root)\
            .foreach(self.vim.switch_root)


@neovim.plugin
class ProteomePlugin(NvimPlugin):

    def __init__(self, vim: neovim.Nvim) -> None:
        super(ProteomePlugin, self).__init__(NvimFacade(vim))

    @neovim.command('ProteomeInit', sync=True, nargs=0)
    def proteome_init(self):
        config_path = self.vim.ps('config_path')\
            .get_or_else('/dev/null')
        bases = self.vim.pl('base_dirs')\
            .get_or_else(List())
        self.pro = Proteome(self.vim, Path(config_path), bases)
        self.vim.vim.call('ptplugin#runtime_after')

    @command()
    def pro_create(self, name, root):
        self.pro.create(name, root)

    @command()
    def pro_add(self, name: str):
        self.pro.add_by_name(name)

    @command(sync=True)
    def pro_show(self, *names):
        Log.info(self.pro.show(List.wrap(names)))

    @command()
    def pro_c_tags(self, *names):
        self.pro.ctags(List.wrap(names))

    @command()
    def pro_to(self, name: str):
        self.pro.switch_root(name)

__all__ = ['ProteomePlugin', 'Proteome']
