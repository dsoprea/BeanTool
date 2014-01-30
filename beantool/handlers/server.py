from pprint import pprint

from beantool.handlers.handler_base import HandlerBase

def register_commands(subparsers):
    parser_serverstats = subparsers.add_parser('server_stats', help='Show server-level statistics')

    parser_serverkick = subparsers.add_parser('server_kick', help='Kick buried job(s)')
# TODO(dustin): Does this take a tube?
    parser_serverkick.add_argument('-c', '--count', default=1, type=int, help='Number of jobs to kick')


class ServerHandler(HandlerBase):
    def stats(self):
        print("Server stats:")
        print('')

        pprint(self.beanstalk.stats())

    def kick(self, count):
        print("Kicking buried jobs.")

        self.beanstalk.kick(count)
