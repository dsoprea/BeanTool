Summary
-------

BeanTool is a console tool for quering your *[beanstalkd](http://kr.github.io/beanstalkd)* server. The name of the executable is *bt*, and provides the following subcommands. You may list the subcommands and their descriptions by running __"bt -h"__.


Installation
------------

1. git clone https://github.com/dsoprea/BeanTool beantool
2. cd beantool
3. sudo python setup.py install


Subcommands
-----------

The subcommands are listed below along with an example. However, there are many options that are not displayed (hostname, tube name, priority, etc..). Each subcommand has its own command-line help.

### server_stats

Show server-level statistics

```bash
$ bt server_stats
```

```
Server stats:

{
  "current-connections": 1,
  "max-job-size": 65535,
  "cmd-release": 11,
  "cmd-reserve": 25,
  "pid": 53138,
  "cmd-bury": 1,
  "current-producers": 0,
  "total-jobs": 14,
  "current-jobs-ready": 0,
  "cmd-peek-buried": 1,
  "current-tubes": 1,
  "id": "e480716f4fc498f8",
  "current-jobs-delayed": 0,
  "uptime": 11274,
  "cmd-watch": 21,
  "hostname": "dustinx",
  "job-timeouts": 0,
  "cmd-stats": 2,
  "rusage-stime": 0.016621,
  "version": 1.9,
  "current-jobs-reserved": 0,
  "current-jobs-buried": 0,
  "cmd-reserve-with-timeout": 11,
  "cmd-put": 14,
  "cmd-pause-tube": 0,
  "cmd-list-tubes-watched": 0,
  "cmd-list-tubes": 4,
  "current-workers": 0,
  "cmd-list-tube-used": 0,
  "cmd-ignore": 0,
  "binlog-records-migrated": 0,
  "current-waiting": 0,
  "cmd-peek": 42,
  "cmd-peek-ready": 8,
  "cmd-peek-delayed": 1,
  "cmd-touch": 0,
  "binlog-oldest-index": 0,
  "binlog-current-index": 0,
  "cmd-use": 26,
  "total-connections": 125,
  "cmd-delete": 15,
  "binlog-max-size": 10485760,
  "cmd-stats-job": 18,
  "rusage-utime": 0.006289,
  "cmd-stats-tube": 11,
  "binlog-records-written": 0,
  "cmd-kick": 0,
  "current-jobs-urgent": 0
}
```

### server_kick

Kick (requeue) buried job(s)

```bash
$ bt server_kick
```

```
Kicking buried jobs.

{
  "kicked": 0
}
```

### tube_list

List tubes

```bash
$ bt tube_list
```

```
Current tubes:

[
  "default"
]
```

### tube_stats

Show tube-level statistics

```bash
$ bt tube_stats default
```

```
Tube stats:

{
  "current-jobs-delayed": 0,
  "pause": 0,
  "name": "default",
  "cmd-pause-tube": 0,
  "current-jobs-buried": 0,
  "cmd-delete": 1,
  "pause-time-left": 0,
  "current-waiting": 0,
  "current-jobs-ready": 0,
  "total-jobs": 1,
  "current-watching": 1,
  "current-jobs-reserved": 0,
  "current-using": 1,
  "current-jobs-urgent": 0
}
```

### job_put

Push a job

```bash
$ bt job_put 'job data'
```

```
Job created:

{
  "job_id": 15
}
```

### job_peek

Peek on a specific job

```bash
$ bt job_peek 15
```

```
<JOB (15)>

job data
```

### job_peek_ready

Peek for 'ready' jobs

```bash
$ bt job_peek_ready
```

```
<JOB (15)>

job data
```

### job_peek_delayed

Peek for 'delayed' jobs

```bash
$ bt job_peek_delayed
```

### job_peek_buried

Peek for 'buried' jobs

```bash
$ bt job_peek_buried
```

### job_stats

Get job stats

```bash
$ bt job_stats 15
```

```
Job stats:

{
  "buries": 0,
  "time-left": 0,
  "releases": 0,
  "tube": "default",
  "timeouts": 0,
  "ttr": 120,
  "age": 566,
  "pri": 2147483648,
  "delay": 0,
  "state": "ready",
  "reserves": 0,
  "file": 0,
  "kicks": 0,
  "id": 15
}
```

### job_delete

Delete job

```bash
$ bt job_delete 15
```

```
Deleted.
```

Notes
-----

1. Human readable text and phrasing is printed to STDERR. Data is printed to STDOUT.
2. Everything written to STDOUT is encoded as JSON, except for job-bodies.
3. The tool works by connecting, running one command, and disconnecting. Therefore, jobs can't be reserved, touched, released, buried, etc.., since *beanstalkd* releases jobs automatically when the client disconnects.
