from beanstalkc import DEFAULT_PRIORITY, DEFAULT_TTR

from beantool.handlers.handler_base import HandlerBase, WrappedJob

def register_commands(subparsers):
    parser_jobput = subparsers.add_parser('job_put', help='Push a job')
    parser_jobput.add_argument('-t', '--tube', help='Tube')
    parser_jobput.add_argument('-p', '--priority', default=DEFAULT_PRIORITY, 
                               type=int, help='Priority')
    parser_jobput.add_argument('-r', '--ttr', default=DEFAULT_TTR, type=int, 
                               help='TTR')
    parser_jobput.add_argument('-d', '--delay', default=0, type=int, help='Delay')
    parser_jobput.add_argument('data', help='Job data')

    parser_jobreserve = subparsers.add_parser('job_reserve', help='Reserve a job')
    parser_jobreserve.add_argument('-t', '--tube', action='append', help='Tube(s)')
    parser_jobreserve.add_argument('-T', '--timeout', type=int, help='Timeout')

    parser_jobpeek = subparsers.add_parser('job_peek', help='Peek on a job')
    parser_jobpeek.add_argument('job_id', type=int, help='ID of specific job')

    parser_jobpeekready = subparsers.add_parser('job_peek_ready', help="Peek for 'ready' jobs")
    parser_jobpeekready.add_argument('-t', '--tube', help='Tube')

    parser_jobpeekdelayed = subparsers.add_parser('job_peek_delayed', help="Peek for 'delayed' jobs")
    parser_jobpeekdelayed.add_argument('-t', '--tube', help='Tube')

    parser_jobpeekburied = subparsers.add_parser('job_peek_buried', help="Peek for 'buried' jobs")
    parser_jobpeekburied.add_argument('-t', '--tube', help='Tube')

# TODO(dustin): All informative output should go to STDERR. All data should go to STDOUT.


class JobHandler(HandlerBase):
    def put(self, data, tube, priority, delay, ttr):
        if tube is not None:
            self.beanstalk.use(tube)

        job_id = self.beanstalk.put(data, priority, delay, ttr)
        print("Job created: %d" % (job_id))

    def peek(self, job_id):
        j = self.get_job_by_id(job_id)

        j = WrappedJob(j)
        self.__dump_job(j)

    def __dump_job(self, j):
        print(j)
        print('')
        print(j.body)

    def __use(self, tube):
        if tube is not None:
            self.beanstalk.use(tube)

    def __watch(self, tubes):
        if tubes is not None:
            if issubclass(tubes.__class__, (list, tuple)) is False:
                tubes = [tubes]

                for tube in tubes:
                    self.beanstalk.watch(tube)

    def peek_ready(self, tube=None):
        self.__use(tube)

        j = self.beanstalk.peek_ready()
        if j is None:
            print("No 'ready' jobs found.")
            return

        j = WrappedJob(j)
        self.__dump_job(j)

    def peek_delayed(self, tube=None):
        self.__use(tube)

        j = self.beanstalk.peek_delayed()
        if j is None:
            print("No 'delayed' jobs found.")
            return

        j = WrappedJob(j)
        self.__dump_job(j)

    def peek_buried(self, tube=None):
        self.__use(tube)

        j = self.beanstalk.peek_buried()
        if j is None:
            print("No 'buried' jobs found.")
            return

        j = WrappedJob(j)
        self.__dump_job(j)

    def reserve(self, tube=None, timeout=None):
        """Allocate a job to work on. A timeout of None means that the call 
        will block.
        """

        self.__watch(tube)
# TODO(dustin): It seems like we can call this many times, rapidly, and get the same job back. Why?
        j = self.beanstalk.reserve(timeout)
        if j is None:
            print("No jobs to reserve.")
            return

        j = WrappedJob(j)
        self.__dump_job(j)

# TODO(dustin): Add a "delete" call.
# TODO(dustin): Add a "stats" call.
# TODO(dustin): Add a "release" call.
# TODO(dustin): Add a "bury" call.
