import sure  # NOQA
from flexmock import flexmock  # NOQA

from proteome import Proteome, List

from tek import Spec  # type: ignore
from tek.test import temp_dir  # type: ignore


class Proteome_(Spec, ):

    def setup(self, *a, **kw):
        super(Proteome_, self).setup(*a, **kw)

    def add_project(self):
        p = Proteome()
        d = temp_dir('project1')
        data = List('some', d)
        p._add_root(data)
        p.projects.projects.should.have.length_of(1)
        pro = list(p.projects.projects.values())[0]
        pro.name.should.equal(data[0])

__all__ = ['Proteome_']
