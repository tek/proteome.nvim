from pathlib import Path

from proteome.project import Projects, Resolver, ProjectLoader

from tryp import List, Map

import pyrsistent  # type: ignore


def field(tpe, **kw):
    return pyrsistent.field(type=tpe, mandatory=True, **kw)


class Env(pyrsistent.PRecord):
    config_path = field(Path)
    bases = field(List)
    projects = field(Projects)
    current_index = field(int, initial=0)

    @property
    def loader(self):
        return ProjectLoader(self.config_path, self.resolver)

    @property
    def resolver(self):
        return Resolver(self.bases, Map())

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.projects
        )

    @property
    def current(self):
        return self.projects[self.current_index]

    @property
    def project_count(self):
        return len(self.projects)

    def inc(self, num):
        new_index = (self.current_index + num) % self.project_count
        return self.set(current_index=new_index)

__all__ = ['Env']
