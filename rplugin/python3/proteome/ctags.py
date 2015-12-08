from typing import Tuple
from proteome.project import Project

from fn import F  # type: ignore

import asyncio
from asyncio.subprocess import PIPE  # type: ignore

from tryp import Map


class CTagsResult(object):

    def __init__(self, success, msg):
        self.success = success
        self.msg = msg

    def __str__(self):
        return ('ctags finished successfully'
                if self.success
                else 'ctags failed: {}'.format(self.msg))


class CTagsJob(object):

    def __init__(self, project: Project, status: asyncio.Future) -> None:
        self.project = project
        self.status = status

    def finish(self, f):
        err, msg = f.result()
        self.status.set_result(CTagsResult(err == 0, msg))


class CTagsExecutor(object):

    def __init__(
            self,
            current: Map[Project, CTagsJob]=Map()
    ) -> None:
        self.current = current

    @asyncio.coroutine
    def process(self, project: Project):
        langs = ','.join(project.ctags_langs)
        tag_file = project.tag_file
        args = [
            '-R',
            '--languages={}'.format(langs),
            '-f',
            str(tag_file),
            str(project.root)
        ]
        return (yield from asyncio.create_subprocess_exec(  # type: ignore
            'ctags',
            *args,
            stdout=PIPE,
            stderr=PIPE,
            cwd=str(project.root),
        ))

    @asyncio.coroutine
    def execute(self, project: Project) -> Tuple[int, str]:
        if project.root.is_dir():
            proc = yield from self.process(project)
            yield from proc.wait()  # type: ignore
            err = yield from proc.stderr.readline()
            result = proc.returncode, err.decode()
        else:
            result = 1, 'not a directory: {}'.format(project.root)
        return result  # type: ignore

    def run(self, project: Project):
        ''' return values of execute are set as result of the task
        returned by ensure_future(), obtainable via task.result()
        '''
        task = asyncio.ensure_future(self.execute(project))  # type: ignore
        job = CTagsJob(project, asyncio.Future())
        task.add_done_callback(job.finish)
        task.add_done_callback(F(self.job_done, job))
        self.current[project] = job
        return job

    def job_done(self, job, status):
        if job.project in self.current:
            self.current.pop(job.project)

    @property
    def ready(self):
        return self.current.is_empty

__all__ = ['CTagsExecutor']
