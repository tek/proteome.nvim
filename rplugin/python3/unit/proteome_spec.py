from pathlib import Path

import sure  # NOQA
from flexmock import flexmock  # NOQA

from proteome import Proteome, Create, Projects
from proteome.project import Project
from proteome.plugins.core import Next, Prev

from tryp import List, Just, _

from unit._support.spec import MockNvimSpec
from unit._support.loader import _LoaderSpec
from unit._support.async import test_loop


class Proteome_(MockNvimSpec, _LoaderSpec):

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

    def command(self):
        class P(Proteome):
            def init(self):
                return dict()
        plug = 'unit._support.test_plug'
        prot = P(self.vim, Path('/dev/null'), List(plug), List())
        data = 'message_data'
        prot.plug_command('test_plug', 'do', [data])
        prot._data.should.have.key(data).being.equal(data)

    def invalid_command(self):
        class P(Proteome):
            def init(self):
                return dict()
        plug = 'unit._support.test_plug'
        prot = P(self.vim, Path('/dev/null'), List(plug), List())
        data = 'message_data'
        prot.plug_command('test_plug', 'do', [data])
        prot.plug_command('test_plug', 'dont', [data])
        prot._data.should.have.key(data).being.equal(data)

    def ctags(self):
        plug_name = 'proteome.plugins.ctags'
        p1 = self.mk_project('pro1', 'c')
        p2 = self.mk_project('pro2', 'go')
        prot = Proteome(self.vim, Path('/dev/null'), List(plug_name), List())
        plug = prot.plugin('ctags')._get
        pros = List(p1, p2)
        prot._data = prot._data.set(projects=Projects(pros))
        p1.tag_file.exists().should_not.be.ok
        p2.tag_file.exists().should_not.be.ok
        with test_loop() as loop:
            prot.plug_command('ctags', 'gen', List())
            plug.ctags.current.values\
                .map(_.status)\
                .foreach(loop.run_until_complete)
        plug.ctags.current.keys.should.be.empty
        p1.tag_file.exists().should.be.ok
        p2.tag_file.exists().should.be.ok

__all__ = ['Proteome_']
