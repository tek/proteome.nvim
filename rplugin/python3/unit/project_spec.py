import sure  # NOQA
from flexmock import flexmock  # NOQA

from fn import _  # type: ignore

from tryp import Just, List

from proteome import Projects
from proteome.project import Project

from unit._support.loader import _LoaderSpec


class Projects_(_LoaderSpec):

    def setup(self, *a, **kw):
        super(Projects_, self).setup(*a, **kw)

    def show(self):
        n = 'some name'
        d = '/dir/to/project'
        p2 = Projects() + Project(n, d)
        p2.show().should.equal(List('{}: {}'.format(n, d)))
        p2.show(List(n)).should.equal(List('{}: {}'.format(n, d)))
        str(p2).should.equal("Projects(Project('{}'))".format(n))


class ProjectLoader_(_LoaderSpec):

    def setup(self, *a, **kw):
        super(ProjectLoader_, self).setup(*a, **kw)

    def resolve(self):
        self.loader \
            .resolve(self.pypro1_type, self.name) \
            .map(_.root) \
            .should.equal(Just(self.pypro1_root))

    def config(self):
        self.loader.config.lift(0)\
            .flat_map(lambda a: a.get('name'))\
            .should.equal(Just(self.name))

    def json_by_name(self):
        self.loader.json_by_name(self.name)\
            .flat_map(lambda a: a.get('type'))\
            .should.equal(Just(self.pypro1_type))

    def from_file(self):
        pj = self.loader.by_name(self.name)
        pj.should.be.a(Just)
        pro = pj._get
        pro.should.be.a(Project)
        pro.name.should.equal(self.name)
        pro.tpe.should.equal(Just(self.pypro1_type))

__all__ = ['Projects_', 'ProjectLoader_']
