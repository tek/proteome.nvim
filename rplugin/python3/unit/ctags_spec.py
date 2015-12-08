import sure  # NOQA
from flexmock import flexmock  # NOQA
from pathlib import Path

from tryp import List, Just

from proteome.project import Project
from proteome.ctags import CTagsExecutor

from unit.project_spec import _LoaderSpec
from unit._support.async import test_loop

from tek.test import temp_path


class CTagsExecutor_(_LoaderSpec):

    def run(self):
        with test_loop() as loop:
            ctags = CTagsExecutor()
            p = Project(self.name, self.pypro1_root,
                        tpe=Just(self.pypro1_type),
                        langs=List(self.pypro1_type))
            p.remove_tag_file()
            job = ctags.run(p)
            result = loop.run_until_complete(job.status)
            result.success.should.be.ok
        p.tag_file.exists().should.be.ok
        ctags.current.keys.should.be.empty

    def fail(self):
        with test_loop() as loop:
            ctags = CTagsExecutor()
            p = Project('invalid', Path(temp_path('invalid')), tpe=Just('c'),
                        langs=List('c'))
            job = ctags.run(p)
            result = loop.run_until_complete(job.status)
            result.success.should_not.be.ok

__all__ = ['CTagsExecutor_']
