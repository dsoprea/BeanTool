from pprint import pformat

from beantool.handlers.handler_base import HandlerBase

def register_commands(subparsers):
    # server_stats

    parser_serverstats = subparsers.add_parser('server_stats', help='Show server-level info')

    # server_kick

    parser_serverkick = subparsers.add_parser('server_kick', help='Kick buried job(s)')
# TODO(dustin): Does this take a tube?
    parser_serverkick.add_argument('-c', '--count', default=1, type=int, help='Number of jobs to kick')


class ServerHandler(HandlerBase):
    def stats(self):
        self.write_human("Server stats:\n")

        stats = self.beanstalk.stats()
        self.write_data(stats)

    def kick(self, count):
        self.write_human("Kicking buried jobs.\n")

        kicked = self.beanstalk.kick(count)
        self.write_data({ 'kicked': kicked })
