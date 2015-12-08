from pathlib import Path

from tek.test import fixture_path, temp_dir  # type: ignore

from tryp import List, Map, Just

from proteome.project import Resolver, ProjectLoader, Project

from unit._support.spec import Spec


class _LoaderSpec(Spec):

    def setup(self, *a, **kw):
        super(_LoaderSpec, self).setup(*a, **kw)
        self.name = 'pypro1'
        self.config = Path(fixture_path('conf'))
        self.project_base = Path(fixture_path('projects'))
        self.pypro1_type = 'python'
        self.pypro1_root = self.project_base / self.pypro1_type / self.name
        self.type1_base = Path(fixture_path('type1_projects'))
        self.res = Resolver(List(self.project_base),
                            Map(dict(type1=self.type1_base)))
        self.loader = ProjectLoader(self.config, self.res)
        self.temp_projects = Path(temp_dir('projects'))

    def mk_project(self, name, tpe):
        root = temp_dir(str(self.temp_projects / 'projects' / name))
        return Project(name, Path(root), tpe=Just(tpe))


__all__ = ['_LoaderSpec']
