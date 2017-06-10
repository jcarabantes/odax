# -*- coding: utf-8 -*-
import sys
try:
    import socks
except ImportError:
    print('\n[-] Error! Install socksipy python module\n')
    sys.exit(1)
import socket
from net.proxy.TorProxyExceptions import TorProxyExceptions


#http://stackoverflow.com/q/27957470
class TorProxySupport:

    def __init__(self, path):

        if (path.find(":") == -1):
            raise TorProxyExceptions(
            'Invalid proxy definition.'
            ' Please use "server:port" instead of "{0}"'
            .format(path))

            sys.exit(1)
        self.proxy_server = path.split(":")[0]
        self.proxy_port = int(path.split(":")[1])

    def set(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4,
            self.proxy_server, self.proxy_port, True)
        socket.socket = socks.socksocket


