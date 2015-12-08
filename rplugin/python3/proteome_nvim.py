import neovim  # type: ignore

from proteome.nvim_plugin import ProteomeNvimPlugin


@neovim.plugin
class Plugin(ProteomeNvimPlugin):
    pass
