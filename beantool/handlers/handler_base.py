from sys import stdout, stderr

from beanstalkc import Connection, Job as Job

class WrappedJob(object):
    def __init__(self, job):
        self.__job = job

    def __getattr__(self, key):
        return getattr(self.__job, key)

    def __str__(self):
        if getattr(self, 'jid', None) is None:
            return ('<JOB (LOOKUP FAILED)>')
        else:
            return ('<JOB (%d)>' % (self.jid))

class HandlerBase(object):
    def __init__(self, args):
        self.__b = Connection(host=args.hostname, port=args.port)

    def __del__(self):
        self.__b.close()

    def write_human(self, message):
        stderr.write(message . "\n")

    def write_data(self, message):
        stdout.write(message)
        stderr.write("\n")

    def get_job_by_id(self, job_id):
        j = self.beanstalk.peek(job_id)
        j = WrappedJob(j)

        self.check_job_valid(j)

        return j

    def check_job_valid(self, job):
        if issubclass(job.__class__, (Job, WrappedJob)) is False:
            raise ValueError("Job is not valid.")
        elif getattr(job, 'jid', None) is None:
            raise KeyError("Job was not found.")

    @property
    def beanstalk(self):
        return self.__b
