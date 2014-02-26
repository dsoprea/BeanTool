from pprint import pformat

from beantool.handlers.handler_base import HandlerBase

def register_commands(subparsers):
    # tube_list

    parser_tubelist = subparsers.add_parser('tube_list', help='List tubes')

    # tube_stats

    parser_tubestats = subparsers.add_parser('tube_stats', help='Show tube-level info')
    parser_tubestats.add_argument('tube', help='Tube')

    # server_kick

    parser_tubekick = subparsers.add_parser('tube_kick', help='Kick buried job(s)')
    parser_tubekick.add_argument('-t', '--tube', help='Tube')
    parser_tubekick.add_argument('-c', '--count', default=1, type=int, help='Number of jobs to kick')


class TubeHandler(HandlerBase):
    def list(self):
        self.write_human("Current tubes:\n")

        tubes = self.beanstalk.tubes()
        self.write_data(tubes)

    def stats(self, tube):
        self.write_human("Tube stats:\n")

# TODO(dustin): If the tube doesn't exist, you'll get an exception:
#   beanstalkc.CommandFailed: ('stats-tube', 'NOT_FOUND', [])

        stats = self.beanstalk.stats_tube(tube)
        self.write_data(stats)

    def kick(self, tube, count):
        self.write_human("Kicking buried jobs.\n")

        if tube is not None:
            self.beanstalk.use(tube)
    
        kicked = self.beanstalk.kick(count)
        self.write_data({ 'kicked': kicked })

# TODO(dustin): Add pause_tube (name, delay).
