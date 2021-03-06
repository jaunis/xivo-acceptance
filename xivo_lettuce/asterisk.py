# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import errno
import fcntl
import logging
import os
import select
import subprocess
import sys
import threading
from lettuce import world

logger = logging.getLogger('acceptance')


def start_ami_monitoring():
    _ami_monitor.start()


def stop_ami_monitoring():
    _ami_monitor.stop()


def fetch_ami_lines():
    return _ami_monitor.fetch_data().splitlines()


class _Pipe(object):

    def __init__(self):
        self.read_fd, self.write_fd = os.pipe()
        self._set_cloexec_flag(self.read_fd)
        self._set_cloexec_flag(self.write_fd)

    def _set_cloexec_flag(self, fd):
        fcntl.fcntl(fd, fcntl.F_SETFD, fcntl.fcntl(fd, fcntl.F_GETFD) | fcntl.FD_CLOEXEC)

    def close(self):
        os.close(self.read_fd)
        os.close(self.write_fd)

    def read(self, buffersize):
        return os.read(self.read_fd, buffersize)

    def write(self, string):
        return os.write(self.write_fd, string)


class _AMIMonitor(object):

    _REMOTE_COMMAND = ['tcpflow', '-C', '-i', 'lo', 'tcp', 'port', '5038']

    def __init__(self):
        self._thread = None
        self._data = ''
        self._pipe = _Pipe()
        self._lock = threading.Lock()

    def start(self):
        if self._thread:
            raise Exception('AMI monitor thread is already running')

        self._data = ''
        p = world.ssh_client_xivo.new_process(self._REMOTE_COMMAND, stdout=subprocess.PIPE)
        try:
            self._thread = threading.Thread(target=self._run, name='AMI monitor', args=(p,))
            self._thread.start()
        except Exception:
	    p.terminate()
	    p.wait()

    def stop(self):
        if not self._thread:
            return

        self._pipe.write('0000')
        self._thread.join()
        self._thread = None

    def fetch_data(self):
        with self._lock:
            data = self._data
            self._data = ''

        return data

    def _run(self, p):
        print_returncode = False
        try:
            poller = select.poll()
            poller.register(p.stdout.fileno(), select.POLLIN)
            poller.register(self._pipe.read_fd, select.POLLIN)
            ok = True
            while ok:
                try:
                    ready = poller.poll()
                except select.error as e:
                    if e.args[0] == errno.EINTR:
                        continue
                    raise

                for fd, mode in ready:
                    if mode & select.POLLIN:
                        if fd == p.stdout.fileno():
                            data = os.read(fd, 2048)
                            if not data:
                                ok = False
                                print_returncode = True
                            else:
                                with self._lock:
                                    self._data += data
                        elif fd == self._pipe.read_fd:
                            if mode & select.POLLIN:
                                self._pipe.read(16)
                                ok = False
                    else:
                        ok = False
                        print_returncode = True
        finally:
            p.terminate()
            p.wait()
            if print_returncode:
                print >> sys.stderr, 'AMI monitoring: process returned %s' % p.returncode


_ami_monitor = _AMIMonitor()
