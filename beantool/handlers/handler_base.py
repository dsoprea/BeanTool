from sys import stdout, stderr
from json import dumps

from beanstalkc import Connection, Job as Job


class HandlerBase(object):
    def __init__(self, args):
        self.__b = Connection(host=args.hostname, port=args.port)

    def __del__(self):
        self.__b.close()

    def get_job_string(self, job):
        if getattr(job, 'jid', None) is None:
            return ('<JOB (LOOKUP FAILED)>')
        else:
            return ('<JOB (%d)>' % (job.jid))

    def write_human(self, message):
        stderr.write(message + "\n")

    def write_data(self, data, encode=True):
        if encode is True:
            data = dumps(data, indent=2, separators=(',', ': '))

        stdout.write(data)
        stdout.write("\n")

    def get_job_by_id(self, job_id):
        j = self.beanstalk.peek(job_id)

        self.check_job_valid(j)

        # beanstalkc does a poor job of tracking (or, rather, guessing) whether 
        # or not a job is properly reserved in order to do most things. Not 
        # only does it just not do anything if not reserved, but this state-
        # tracking doesn't at all work for our use case (one-offs).
        j.reserved = True

        return j

    def check_job_valid(self, job):
        if job is None:
            raise KeyError("Job was not found (1).")
        elif issubclass(job.__class__, Job) is False:
            raise ValueError("Job is not valid.")
        elif getattr(job, 'jid', None) is None:
            raise KeyError("Job was not found (2).")

    @property
    def beanstalk(self):
        return self.__b
