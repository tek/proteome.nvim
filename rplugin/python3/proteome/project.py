from pathlib import Path
import json
import os

from tryp import Maybe, Empty, Just, List, Map, may

from fn import _  # type: ignore

from trypnv import Log


class Project(object):

    def __init__(
            self,
            name: str,
            root: Path,
            tpe: Maybe[str]=Empty(),
            types: List[str]=List(),
            langs: List[str]=List(),
    ) -> None:
        self.name = name
        self.root = root
        self.tpe = tpe
        self.types = types
        self.langs = langs

    @property
    def info(self) -> str:
        return '{}: {}'.format(self.name, self.root)

    def __str__(self):
        return self.info

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.name))


class Projects(object):

    def __init__(self, projects: Map[str, Project]=Map()) -> None:
        self.projects = projects

    def __add__(self, pro: Project) -> 'Projects':
        return Projects(self.projects + (pro.name, pro))

    def __pow__(self, pro: List[Project]) -> 'Projects':
        pros = Map(pro.map(lambda a: (a.name, a,)))
        return Projects(self.projects ** pros)

    def show(self, names: List[str]=List()):
        if names.isEmpty:
            pros = self.projects.values
        else:
            pros = names.flatMap(self.projects.get)
        return pros.map(_.info)

    def project(self, name: str) -> Maybe[Project]:
        return self.projects.get(name)

    def ctags(self, pros: List):
        matching = pros.map(self.project).flatMap(_.toList)
        return matching

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ','.join(map(repr, self.projects.values()))
        )


class Resolver(object):

    def __init__(self, bases: List[Path], types: Map[str, Path]) -> None:
        self.bases = bases
        self.types = types

    def type_name(self, tpe: str, name: str):
        return self.bases.map(_ / tpe / name).find(_.is_dir)


class ProjectLoader(object):

    def __init__(self, config_path: Path, resolver: Resolver) -> None:
        self.resolver = resolver
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> List[Map]:
        def parse(path: Path):
            with path.open() as f:
                try:
                    return List.wrap(map(Map, json.loads(f.read())))
                except Exception as e:
                    Log.error('parse error in {}: {}'.format(path, e))
                    return List()
        if (self.config_path.is_dir()):
            return List.wrap(self.config_path.glob('*.json')) \
                .flatMap(parse)
        else:
            return parse(self.config_path)

    def resolve(self, tpe: str, name: str):
        return self.resolver.type_name(tpe, name) \
            .map(lambda a: Project(name, a))

    def json_by_name(self, name: str):
        return self.config \
            .find(lambda a: a.get('name').contains(name))

    def by_name(self, name: str):
        return self.json_by_name(name)\
            .flatMap(self._from_json)

    def _from_json(self, json: Map) -> Maybe[Project]:
        def from_type(tpe: str, name: str):
            root = json.get('root') \
                .map(os.path.expanduser)\
                .get_or_else(self.resolver.type_name(tpe, name))
            return Project(name, root, Just(tpe))
        return json.get('type') \
            .zip(json.get('name')) \
            .smap(from_type)

    @may
    def create(self, name: str, root: Path, **kw):
        if root.is_dir():
            return Project(name, root, **kw)

__all__ = ['Projects', 'Project', 'ProjectLoader', 'Resolver']
