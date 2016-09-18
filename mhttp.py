# Demo MicroPython Class for HTTP Post
# Version 0.1
# Disclaimer: This is not an official Splunk solution and with no liability. Use at your own risk.
# For feedback and bug report, please send to jyung@splunk.com

import socket
import ure

class InvalidHost(Exception):
    pass

class InvalidPort(Exception):
    pass

class ConnectionFailed(Exception):
    pass

class http(object):
    class InvalidHost(InvalidHost):
        pass

    class InvalidPort(InvalidPort):
        pass

    class ConnectionFailed(ConnectionFailed):
        pass

    def __init__(self):
        self.resp = ""
        self.port = 80
        self.host = ""
        self.uri = ""
        self.header = ""
        self.payload = ""
        self.addr = ""
        self.http = "http"

    def __post(self):
        try:
            s = socket.socket()
            s.connect(self.addr)
            h = "POST %s HTTP/1.1\r\nHost: %s:%s\r\n" % (self.uri, self.host, self.port) + self.header
            s.send(bytes(h + '\r\nContent-Length:%s\r\n\r\n' % len(self.payload) + self.payload + '\r\n', 'utf8'))
            while True:
                r = s.recv(768).decode('utf-8')
                s.close()
                self.resp = r.split('\n')[-1]
                return ure.match(r'HTTP\/1\.1\s(\d+)\s', r).group(1)
        except OSError as e:
            s.close()
            raise ConnectionFailed

    def open(self, url, header="", data=""):
        _, _, self.host, self.uri = url.split('/', 3)
        try:
            self.port = int(self.host.split(':')[1])
            if (self.port < 1024) and (self.port > 65535):
                raise InvalidPort
        except IndexError:
            self.port = 80
        self.host = self.host.split(':')[0]
        try:
            self.addr = socket.getaddrinfo(self.host, self.port)[0][-1]
        except OSError as e:
            raise InvalidHost
        self.uri = '/'+self.uri
        self.header = header
        if data:
            self.payload = data
            return self.__post()
        else:
            return False  # only POST method is implemented

    def read(self):
        return self.resp
