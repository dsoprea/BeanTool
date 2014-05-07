# beantool: Beanstalk console client.
# Copyright (C) 2014  Dustin Oprea
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

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
