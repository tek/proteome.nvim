import neovim  # type: ignore

from proteome import ProteomePlugin


@neovim.plugin
class Plugin(ProteomePlugin):
    pass
