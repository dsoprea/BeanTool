#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import argparse

from beanstalkc import DEFAULT_HOST, DEFAULT_PORT

from beantool import handlers

parser = argparse.ArgumentParser(description='beanstalkd console client.')

parser.add_argument('-H', '--hostname', default=DEFAULT_HOST, 
                    help='Beanstalk hostname')
parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int, 
                    help='Beanstalk port')

subparsers = parser.add_subparsers(help='Subcommand help', dest='subcommand')

# TODO(dustin): Add subcommands for 'touch' and 'time-to-run'.
# TODO(dustin): Add subcommands for job-specific functions, now that we know we can retrieve jobs.
# TODO(dustin): We're not sure that we're handling errors in each method, effectively.
# TODO(dustin): Can we move these argument configurations to each handler?

handlers.server.register_commands(subparsers)
handlers.tube.register_commands(subparsers)
handlers.job.register_commands(subparsers)

args = parser.parse_args()

# Determine what will handle the request.

parts = args.subcommand.split('_')
handler_name = parts[0][0].upper() + parts[0][1:] + 'Handler'
method = '_'.join(parts[1:])

cls = getattr(handlers, handler_name)
handler = cls(args)

# Build the keyword arguments.

params = {}
params.update(args.__dict__)
del params['hostname']
del params['port']
del params['subcommand']

# Handle it.

getattr(handler, method)(**params)
print('')
