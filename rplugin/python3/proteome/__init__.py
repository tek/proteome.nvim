import neovim  # type: ignore

from tryp import Empty, List

from proteome.project import Projects


class Proteome(object):

    def __init__(self):
        self.projects = Projects()
        self._current_index = Empty()

    def _add_root(self, args: List):
        return args.lift(0) \
            .flatMap(lambda n: args.lift(1).map(lambda r: (n, r,))) \
            .flatMap(lambda v: self.projects.add(v[0], v[1]))


@neovim.plugin
class ProteomePlugin(Proteome):

    def __init__(self, vim: neovim.Nvim) -> None:
        self.vim = vim

    @neovim.command('ProteomeInit', sync=True, nargs=0)
    def init_python(self):
        self.vim.vars['proteome#_channel_id'] = self.vim.channel_id

    @neovim.command('PAdd', sync=False, nargs='+')
    def add_root(self, args: list):
        self._add_root(List.wrap(args))

    @neovim.command('PShow', sync=False, nargs='?')
    def show(self, name: str=None):
        self.projects.show(name)

    @neovim.command('CTags', sync=False, nargs='*')
    def ctags(self, names: list):
        self.projects.ctags(List.wrap(names))

__all__ = ['ProteomePlugin']
