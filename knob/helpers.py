from Exscript.protocols import Telnet, SSH2
from Exscript import Account
from django.conf import settings
from contextlib import contextmanager
from celery import chord
from celery.utils import uuid
from paramiko import SSHException

import socket
import logging
import math
import re

logger = logging.getLogger(__name__)


@contextmanager
def socket_context(*args, **kwargs):
    s = socket.socket(*args, **kwargs)
    try:
        yield s
    finally:
        s.close()


class ConnectionHandler(object):
    def __init__(self, host_address, username, password):
        self.host_address = host_address
        self.username = username
        self.password = password
        self.handler = self._get_connection_handler()


    def _get_connection_handler(self):
        """Factory method to determine the proper connection, it tries to establish an ssh connection with the
        target ip, if it succeeds, the operation is done through ssh, otherwise it's done through telnet"""
        with socket_context(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host_address, 22))
                logger.debug("Port 22 reachable, Checking SSH version")
                s.send("SSH-2.0-billsSSH_3.6.3q3 \r\n")  # send some identifier with the supported version in order
                # to get the ssh version on server
                output = s.recv(1024)
                match = re.match(r"SSH-(\d+.\d+)-*", output)
                version = float(match.group(1))
                if version < 2.0:
                    logger.warn("SSh version %s not supported ... Falling back to Telnet", version)
                    return Telnet
                return SSH2

            except socket.error:
                logger.warn("can't connect to port 22, trying Telnet")

        with socket_context(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host_address, 23))
                logger.debug("Port 23 reachable, I'll use Telnet !")
                return Telnet

            except socket.error as e:
                logger.warn("can't connect to port 23, can't connect to host %s", self.host_address)
                raise



    def __enter__(self):
        self.account = Account(self.username, password=self.password)
        self.conn = self.handler(debug=settings.CONNECTION_DEBUG_LEVEL, connect_timeout=None)
        self.conn.connect(self.host_address)
        self.conn.login(self.account)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.send('exit\r')
        self.conn.close(force=True)

    def execute(self, command):
        self.conn.execute(command)
        return self.conn.response


def chunks(all_ips, available_workers, telnet_commands, username, password, python_shell):
    """Yield successive chunks from list all_ips with required arguments to process the destination ips uniformly distributed among workers."""
    chunk_size = int(math.ceil(float(len(all_ips)) / available_workers))

    for i in xrange(0, len(all_ips), chunk_size):
        yield all_ips[i:i+chunk_size], telnet_commands, username, password, python_shell



class ProgressChord(chord):
    """A proxy class that results in a chord that keeps track of the results"""
    def __call__(self, body=None, **kwargs):
        _chord = self.chord
        body = (body or self.kwargs['body']).clone()
        kwargs = dict(self,kwargs, body=body, **kwargs)
        if _chord.app.conf.CELERY_ALWAYS_EAGER:
            return self.apply((), kwargs)
        callback_id = body.options.setdefault('task_id', uuid())
        r = _chord(**kwargs)
        return _chord.AsyncResult(callback_id), r


def flat_map(nested):
    return [y for x in nested for y in x]