from toolz import dicttoolz  # type: ignore

from trypnv.machine import may_handle, message

from proteome.state import ProteomeComponent

Do = message('Do', 'msg')


class Plugin(ProteomeComponent):

    @may_handle(Do)
    def doit(self, env: dict, msg):
        return dicttoolz.merge(env, {msg.msg: msg.msg})


__all__ = ['Plugin']
