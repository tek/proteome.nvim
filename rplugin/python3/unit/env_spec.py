import sure  # NOQA
from flexmock import flexmock  # NOQA

from tryp import List

from proteome.env import Env
from proteome import Projects

from unit.project_spec import _LoaderSpec


class Env_(_LoaderSpec, ):

    def setup(self, *a, **kw):
        super(Env_, self).setup(*a, **kw)
        self.env = Env(self.loader, Projects())

    def load_project(self):
        e1 = self.env
        e2 = e1.load(List('pypro1'))
        e2.projects.projects.should.have.length_of(1)

__all__ = ['Env_']
