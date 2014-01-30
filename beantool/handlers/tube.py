from beantool.handlers.handler_base import HandlerBase

def register_commands(subparsers):
    parser_tubelist = subparsers.add_parser('tube_list', help='List tubes')

    parser_tubestats = subparsers.add_parser('tube_stats', help='Show tube-level statistics')
    parser_tubestats.add_argument('tube', help='Tube')


class TubeHandler(HandlerBase):
    def list(self):
        print(self.beanstalk.tubes())
