from pathlib import Path

import sure  # NOQA
from flexmock import flexmock  # NOQA

from proteome import Proteome, Create, Projects
from proteome.project import Project
from proteome.plugins.core import Next, Prev

from tryp import List, Just

from unit._support.spec import MockNvimSpec


class Proteome_(MockNvimSpec):

    def create(self):
        name = 'proj'
        root = Path('/dev/null')
        prot = Proteome(self.vim, root, List(), List())
        prot.send(Create(name, root))
        p = prot._data.projects.projects[0]
        p.name.should.equal(name)
        p.root.should.equal(root)

    def cycle(self):
        self.vim_mock.should_receive('switch_root').and_return(None)
        name = 'proj'
        name2 = 'proj2'
        root = Path('/dev/null')
        prot = Proteome(self.vim, root, List(), List())
        pros = List(Project(name, root), Project(name2, root))
        prot._data = prot._data.set(projects=Projects(pros))
        prot._data.current.should.equal(Just(pros[0]))
        prot.send(Next())
        prot._data.current.should.equal(Just(pros[1]))
        prot.send(Prev())
        prot._data.current.should.equal(Just(pros[0]))

__all__ = ['Proteome_']
