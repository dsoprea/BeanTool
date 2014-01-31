import sys

from beanstalkc import DEFAULT_PRIORITY, DEFAULT_TTR

from beantool.handlers.handler_base import HandlerBase, catch_notfound
from beantool.job_terminal import JobTerminal

def register_commands(subparsers):
    # job_put

    parser_jobput = subparsers.add_parser('job_put', help='Push a job')
    parser_jobput.add_argument('-t', '--tube', help='Tube')
    parser_jobput.add_argument('-p', '--priority', default=DEFAULT_PRIORITY, 
                               type=int, help='Priority')
    parser_jobput.add_argument('-r', '--ttr', default=DEFAULT_TTR, type=int, 
                               help='TTR')
    parser_jobput.add_argument('-d', '--delay', default=0, type=int, help='Delay')
    parser_jobput.add_argument('data', help="Job data ('-' to read from STDIN)")

    # job_reserve

    parser_jobreserve = subparsers.add_parser('job_reserve', help='Reserve a job')
    parser_jobreserve.add_argument('-t', '--tube', action='append', help='Tube(s)')
    parser_jobreserve.add_argument('-T', '--timeout', type=int, help='Timeout')

    # job_peek

    parser_jobpeek = subparsers.add_parser('job_peek', help='Peek on a specific job')
    parser_jobpeek.add_argument('job_id', type=int, help='ID of specific job')

    # job_peek_ready

    parser_jobpeekready = subparsers.add_parser('job_peek_ready', help="Peek for 'ready' jobs")
    parser_jobpeekready.add_argument('-t', '--tube', help='Tube')

    # job_peek_delayed

    parser_jobpeekdelayed = subparsers.add_parser('job_peek_delayed', help="Peek for 'delayed' jobs")
    parser_jobpeekdelayed.add_argument('-t', '--tube', help='Tube')

    # job_peek_buried

    parser_jobpeekburied = subparsers.add_parser('job_peek_buried', help="Peek for 'buried' jobs")
    parser_jobpeekburied.add_argument('-t', '--tube', help='Tube')

    # job_stats

    parser_jobstats = subparsers.add_parser('job_stats', help="Show job-level info")
    parser_jobstats.add_argument('job_id', type=int, help='ID of specific job')

    # job_delete

    parser_jobdelete = subparsers.add_parser('job_delete', help="Delete job")
    parser_jobdelete.add_argument('job_id', type=int, help='ID of specific job')


class JobHandler(HandlerBase):
    def __dump_job(self, j):
        self.write_human(self.get_job_string(j) + "\n")
        self.write_data(j.body, encode=False)

    def __use(self, tube):
        if tube is not None:
            self.beanstalk.use(tube)

    def __watch(self, tubes):
        if tubes is not None:
            if issubclass(tubes.__class__, (list, tuple)) is False:
                tubes = [tubes]

            for tube in tubes:
                self.beanstalk.watch(tube)

    def put(self, data, tube, priority, delay, ttr):
        if tube is not None:
            self.beanstalk.use(tube)

        if data == '-':
            data = sys.stdin.read()

        job_id = self.beanstalk.put(data, priority, delay, ttr)
        self.write_human("Job created:\n")
        self.write_data({ 'job_id': job_id })

    @catch_notfound
    def peek(self, job_id):
        j = self.beanstalk.peek(job_id)
        if j is None:
            self.write_human("No 'ready' jobs found.")
            return

        self.__dump_job(j)

    def peek_ready(self, tube=None):
        self.__use(tube)

        j = self.beanstalk.peek_ready()
        if j is None:
            self.write_human("No 'ready' jobs found.")
            return

        self.__dump_job(j)

    def peek_delayed(self, tube=None):
        self.__use(tube)

        j = self.beanstalk.peek_delayed()
        if j is None:
            self.write_human("No 'delayed' jobs found.")
            return

        self.__dump_job(j)

    def peek_buried(self, tube=None):
        self.__use(tube)

        j = self.beanstalk.peek_buried()
        if j is None:
            self.write_human("No 'buried' jobs found.")
            return

        self.__dump_job(j)

    def reserve(self, tube=None, timeout=None):
        """Allocate a job to work on, and send us into a "command terminal" 
        with a sustained connection to beanstalkd.
        """

        self.__watch(tube)

        print("Requesting job.")

        j = self.beanstalk.reserve(timeout)
        if j is None:
            self.write_human("No jobs to reserve.")
            return

        print('')
        JobTerminal(self.beanstalk, j).run_loop()

    @catch_notfound
    def stats(self, job_id):
        j = self.build_job(job_id)

        self.write_human("Job stats:\n")
        self.write_data(j.stats())

    @catch_notfound
    def delete(self, job_id):
        j = self.build_job(job_id)
        j.delete()

        self.write_human("Deleted.")
