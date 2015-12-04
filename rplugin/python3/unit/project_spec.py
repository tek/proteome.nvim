from pathlib import Path

import sure  # NOQA
from flexmock import flexmock  # NOQA

from fn import _  # type: ignore

from tek import Spec  # type: ignore
from tek.test import temp_dir, fixture_path  # type: ignore

from tryp import List, Map, Just

from proteome import Projects
from proteome.project import ProjectLoader, Resolver


class Projects_(Spec, ):

    def setup(self, *a, **kw):
        super(Projects_, self).setup(*a, **kw)

    def valid_path(self):
        p = Projects()
        d = temp_dir('project1')
        err = p.add('some', d)
        err.isJust.should_not.be.ok
        pro = list(p.projects.values())[0]
        str(pro.root).should.equal(d)

    def invalid_path(self):
        p = Projects()
        err = p.add('name', '/tmp/invalidpath')
        err.isJust.should.be.ok


class ProjectLoader_(Spec, ):

    def setup(self, *a, **kw):
        super(ProjectLoader_, self).setup(*a, **kw)
        self.name = 'pypro1'
        self.config = Path(fixture_path('conf'))
        self.project_base = Path(fixture_path('projects'))
        self.pypro1_type = 'python'
        self.pypro1_root = self.project_base / self.pypro1_type / self.name
        self.type1_base = Path(fixture_path('type1_projects'))
        self.res = Resolver(List(self.project_base),
                            Map(type1=self.type1_base))
        self.loader = ProjectLoader(self.config, self.res)

    def resolve(self):
        self.loader \
            .resolve(self.pypro1_type, self.name) \
            .map(_.root) \
            .should.equal(Just(self.pypro1_root))

    def config(self):
        self.loader.config.lift(0)\
            .flatMap(lambda a: a.get('name'))\
            .should.equal(Just(self.name))

    def json_by_name(self):
        self.loader.json_by_name(self.name)\
            .flatMap(lambda a: a.get('type'))\
            .should.equal(Just(self.pypro1_type))

    def from_file(self):
        pro = self.loader.by_name(self.name)
        pro.map(_.name).should.equal(Just(self.name))
        pro.flatMap(_.tpe).should.equal(Just(self.pypro1_type))

__all__ = ['Projects_']
