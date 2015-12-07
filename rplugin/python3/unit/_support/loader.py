from pathlib import Path

from tek.test import fixture_path  # type: ignore

from tryp import List, Map

from proteome.project import Resolver, ProjectLoader

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
                            Map(type1=self.type1_base))
        self.loader = ProjectLoader(self.config, self.res)


__all__ = ['_LoaderSpec']
