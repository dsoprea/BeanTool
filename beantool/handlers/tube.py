from pprint import pformat

from beantool.handlers.handler_base import HandlerBase

def register_commands(subparsers):
    # tube_list

    parser_tubelist = subparsers.add_parser('tube_list', help='List tubes')

    # tube_stats

    parser_tubestats = subparsers.add_parser('tube_stats', help='Show tube-level statistics')
    parser_tubestats.add_argument('tube', help='Tube')


class TubeHandler(HandlerBase):
    def list(self):
        self.write_human("Current tubes:\n")

        tubes = self.beanstalk.tubes()
        self.write_data(tubes)

    def stats(self, tube):
        self.write_human("Tube stats:\n")

        stats = self.beanstalk.stats_tube(tube)
        self.write_data(stats)
