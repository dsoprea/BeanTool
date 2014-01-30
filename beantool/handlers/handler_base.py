import beanstalkc

from sys import stdout, stderr
from json import dumps

from beanstalkc import Connection, Job

def catch_notfound(f):
    """A decorator to produce KeyErrors where necessary."""

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except beanstalkc.CommandFailed as e:
            # Translate a 'NOT_FOUND' error to a KeyError.
            if issubclass(e.args.__class__, tuple) is True and \
               e.args[1] == 'NOT_FOUND':
                raise KeyError()

            raise

    return wrapper


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

    def build_job(self, job_id, body=None):

        # beanstalkc does a poor job of tracking (or, rather, guessing) whether 
        # or not a job is properly reserved in order to do most things. Not 
        # only does it just not do anything if not reserved, but this state-
        # tracking doesn't at all work for our use case (one-offs). We set
        # 'reserved' to True no matter what.

        return Job(self.__b, job_id, body, True)

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
