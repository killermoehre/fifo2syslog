#!/usr/bin/python2
# License:  GPL2+
# Author:   Silvio Knizek <knizek@b1-systems.de>

# This script reads out of a FIFO into syslog.

import sys, os, syslog
from optparse import OptionParser

def doublefork(pid_file):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
    	
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
        
    sys.stdout.flush()
    sys.stderr.flush()
    si = open("/dev/null", "r")
    so = open("/dev/null", "a+")
    se = open("/dev/null", "a+")
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    
    pid = os.getpid()
    try:
        pid_file = open(options.pid_file, "w").write("%s\n" % pid)
    except OSError, e:
        syslog.openlog("syslog", 0, syslog.LOG_DAEMON)
        syslog.syslog(syslog.LOG_ERR, "Writing pid file %s failed: %d (%s)\n" % (pid_file, e.errno, e.strerror))
        syslog.closelog()
        sys.exit(2)
    else:
        pid_file.close()

facility2int = {"LOG_KERN": 0, "LOG_USER": 8, "LOG_MAIL": 16, "LOG_DAEMON": 24, "LOG_AUTH": 32, "LOG_AUTHPRIV": 32, "LOG_SYSLOG": 40, "LOG_LPR": 48, "LOG_NEWS": 56, "LOG_UUCP": 64, "LOG_CRON": 72, "LOG_LOCAL0": 128, "LOG_LOCAL1": 136, "LOG_LOCAL2": 144, "LOG_LOCAL3": 152, "LOG_LOCAL4": 160, "LOG_LOCAL5": 168, "LOG_LOCAL6": 176, "LOG_LOCAL7": 184}
level2int = {"LOG_DEBUG": 7, "LOG_INFO": 6, "LOG_NOTICE": 5, "LOG_WARNING": 4, "LOG_ERR": 3, "LOG_CRIT": 2, "LOG_ALERT": 1, "LOG_EMERG": 0}

parser = OptionParser()
parser.add_option("-d", "--daemonize", dest="daemonize", action="store_true", default=False, help="Daemonize or not.")
parser.add_option("-f", "--fifo", dest="source_fifo", default=False, help="The source FIFO we should read from.", metavar="/path/to/file")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Print the messages additional to STDOUT")
parser.add_option("--pid", dest="pid_file", default="/var/run/fifo2syslog.pid", help="PID file to use", metavar="/path/to/file")
parser.add_option("--facility", dest="syslog_facility", choices=facility2int.keys(), default="LOG_USER", help="syslog FACILITY to use (see SYSLOG(3))")
parser.add_option("--level", dest="syslog_level", choices=level2int.keys(), default="LOG_INFO", help="syslog LEVEL to use (see SYSLOG(3))")
parser.add_option("--tag", dest="syslog_tag", default="syslog", help="the TAG prepending every line (see LOGGER(1))", metavar="STRING")

(options, args) = parser.parse_args()

if not options.source_fifo:
	sys.stderr.write("Path to FIFO required. Aborting.\n")
	sys.exit(3)

if options.daemonize:
    doublefork(options.pid_file)

try:
    fifo = open(options.source_fifo)
except OSError, e:
    syslog.openlog("syslog", 0, syslog.LOG_DAEMON)
    syslog.syslog(syslog.LOG_ERR, "Reading FIFO %s failed: %d (%s)\n" % (options.source_fifo, e.errno, e.strerror))
    syslog.closelog()
    sys.exit(4)

syslog.openlog(options.syslog_tag, 0, facility2int[options.syslog_facility])
while True:
    message = fifo.readline()
    syslog.syslog(level2int[options.syslog_level], message)
    if options.verbose:
        sys.stdout.write(message)

sys.exit(0)