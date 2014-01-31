from pprint import pformat

from beantool.handlers.handler_base import HandlerBase

def register_commands(subparsers):
    # server_stats

    parser_serverstats = subparsers.add_parser('server_stats', help='Show server-level info')


class ServerHandler(HandlerBase):
    def stats(self):
        self.write_human("Server stats:\n")

        stats = self.beanstalk.stats()
        self.write_data(stats)
