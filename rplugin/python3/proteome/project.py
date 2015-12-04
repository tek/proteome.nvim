from pathlib import Path
import json

from tryp import Maybe, Empty, Just, List, Map

from fn import _  # type: ignore


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

    def __init__(self) -> None:
        self.projects = Map()  # type: Map[str, Project]

    def add(self, name: str, root: str) -> Maybe:
        path = Path(root)
        if path.is_dir():
            self.projects[name] = Project(name, path)
            return Empty()
        else:
            return Just('{} is not a directory'.format(root))

    def show(self, name: str=None):
        return self.projects.get(name) \
            .map(list) \
            .get_or_else(List.wrap(self.projects.values())) \
            .map(_.info)

    def project(self, name: str) -> Maybe[Project]:
        return self.projects.get(name)

    def ctags(self, pros: List):
        matching = pros.map(self.project).flatMap(_.toList)
        return matching


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
                return List.wrap(map(lambda a: Map(**a), json.load(f)))
        if (self.config_path.is_dir()):
            return List.wrap(self.config_path.glob('*.json')) \
                .flatMap(parse)
        else:
            return List()

    def resolve(self, tpe: str, name: str):
        return self.resolver.type_name(tpe, name) \
            .map(lambda a: Project(name, a))

    def json_by_name(self, name: str):
        return self.config \
            .find(lambda a: a.get('name').contains(name))

    def by_name(self, name: str):
        return self.json_by_name(name)\
            .flatMap(self.from_json)

    def from_json(self, json: Map):
        def from_type(tpe: str, name: str):
            root = json.get('root') \
                .or_else(self.resolver.type_name(tpe, name))
            return Project(name, root, Just(tpe))
        return json.get('type') \
            .zip(json.get('name')) \
            .smap(from_type)

__all__ = ['Projects', 'Project', 'ProjectLoader', 'Resolver']
