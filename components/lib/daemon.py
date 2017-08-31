import json
import sys
import os
import time
import atexit
from signal import SIGTERM

import redis


class Daemon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method.
    """

    def __init__(self,
                 stdin='/dev/null',
                 stdout='/dev/null',
                 stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.redis_instance = redis.StrictRedis()
        self.process_id = None

    def daemonize(self):
        """
        daemonize method to use UNIX double-fork magic.
        for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            self.process_id = os.fork()
            if self.process_id > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: {} ({})\n".format(e.errno,
                                                                e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            self.process_id = os.fork()
            if self.process_id > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: {} ({})\n".format(e.errno,
                                                                e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        standard_in = file(self.stdin, 'r')
        standard_out = file(self.stdout, 'a+')
        standard_err = file(self.stderr, 'a+', 0)
        os.dup2(standard_in.fileno(), sys.stdin.fileno())
        os.dup2(standard_out.fileno(), sys.stdout.fileno())
        os.dup2(standard_err.fileno(), sys.stderr.fileno())

        # write process id into redis
        self.process_id = os.getpid()
        atexit.register(self.delete_process_id)
        process_data = {}
        process_data['name'] = str(__file__)
        process_data['process_id'] = self.process_id
        self.redis_instance.set(self.process_id, json.dumps(process_data))

    def delete_process_id(self):
        if self.process_id is not None:
            self.redis_instance.delete(self.process_id)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            if self.process_id is not None and self.redis_instance.get(self.process_id) is not None:
                raise IOError
        except IOError:
            message = "Daemon already running?\n"
            sys.stderr.write(message)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        stop method to stop the daemon
        """
        try:
            if self.process_id is None or self.redis_instance.get(self.process_id) is None:
                raise IOError('process does not exist.')
        except IOError:
            self.process_id = None

        if not self.process_id:
            message = "process id not found in redis or already None. Daemon not running?\n"
            sys.stderr.write(message)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(self.process_id, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if self.redis_instance.get(self.process_id) is not None:
                    self.redis_instance.delete(self.process_id)
                    self.process_id = None
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        run method, to be overridden by the subclass, in order
        to execute the code under daemon
        """
