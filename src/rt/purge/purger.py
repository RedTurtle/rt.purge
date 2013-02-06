"""The following is borrowed heavily from Products.CMFSquidTool. That code
is ZPL licensed.

Asynchronous purging works as follows:
  
* Each remote host gets a queue and a worker thread.

* Each worker thread manages its own connection.  The queue is not processed
  until it can establish a connection.  Once a connection is established, the
  queue is purged one item at a time. Should the connection fail, the worker
  thread again waits until a connection can be re-established.
"""

import sys
import socket
import httplib
import urlparse
import threading

from zope.interface import implements
from rt.purge.interfaces import IPurger
from rt.purge import logger

class Connection(httplib.HTTPConnection):
    """A connection that can handle either HTTP or HTTPS
    """

    def __init__(self, host, port=None, strict=None, scheme="http", timeout=5):
        self.scheme = scheme
        if scheme == "http":
            self.default_port = httplib.HTTP_PORT
        elif scheme == "https":
            self.default_port = httplib.HTTPS_PORT
        else:
            raise ValueError, "Invalid scheme '%s'" % (scheme,)
        httplib.HTTPConnection.__init__(self, host, port, strict)
        self.timeout = timeout

    def connect(self):
        if self.scheme == "http":
            httplib.HTTPConnection.connect(self)
        elif self.scheme == "https":
            # Clone of httplib.HTTPSConnection.connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            key_file = cert_file = None
            ssl = socket.ssl(sock, key_file, cert_file)
            self.sock = httplib.FakeSocket(sock, ssl)
        else:
            raise ValueError, "Invalid scheme '%s'" % (self.scheme,)
        # Once we have connected, set the timeout.
        self.sock.settimeout(self.timeout)

class DefaultPurger(object):
    """Default purging implementation
    """
    
    implements(IPurger)
    
    def __init__(self, factory=Connection, timeout=30, backlog=200, errorHeaders=('x-squid-error',), http_1_1=True):
        self.factory = factory
        self.timeout = timeout
        self.queues = {}
        self.workers = {}
        self.backlog = backlog
        self.queueLock = threading.Lock()
        self.errorHeaders = errorHeaders
        self.http_1_1 = http_1_1
    
    # Public API
    
    def purgeSync(self, url, httpVerb='PURGE'):
        try:
            conn = self.getConnection(url)
            try:
                resp, xcache, xerror = self._purgeSync(conn, url, httpVerb)
                status = resp.status
            finally:
                conn.close()
        except:
            status = "ERROR"
            err, msg, tb = sys.exc_info()
            from traceback import format_exception
            xerror = '\n'.join(format_exception(err, msg, tb))
            # Avoid leaking a ref to traceback.
            del err, msg, tb
            xcache = ''
        logger.debug('Finished %s for %s: %s %s'
                     % (httpVerb, url, status, xcache))
        if xerror:
            logger.debug('Error while purging %s:\n%s' % (url, xerror))
        logger.debug("Completed synchronous purge of %s", url)
        return status, xcache, xerror
    
    # Internal API between Purger and worker threads
    
    def getConnection(self, url):
        """Creates a new connection - returns a connection object that is
        already connected. Exceptions raised by that connection are not
        trapped.
        """
        
        (scheme, host, path, params, query, fragment) = urlparse.urlparse(url)
        # 
        # process.
        conn = self.factory(host, scheme=scheme, timeout=self.timeout)
        conn.connect()
        logger.debug("established connection to %s", host)
        return conn

    def _purgeSync(self, conn, url, httpVerb):
        """Perform the purge request. Returns a triple
        ``(resp, xcache, xerror)`` where ``resp`` is the response object for
        the connection, ``xcache`` is the contents of the X-Cache header,
        and ``xerror`` is the contents of the first header found of the
        header list in ``self.errorHeaders``.
        """
        
        (scheme, host, path, params, query, fragment) = urlparse.urlparse(url)
        #__traceback_info__ = (url, httpVerb, scheme, host,
        #                      path, params, query, fragment)
        
        if self.http_1_1:
            conn._http_vsn = 11
            conn._http_vsn_str = 'HTTP/1.1'
        else:
            conn._http_vsn = 10
            conn._http_vsn_str = 'HTTP/1.0'
            # When using HTTP 1.0, to make up for the lack of a 'Host' header
            # we use the full url as the purge path, to allow for virtual
            # hosting in squid
            path = url
       
        purge_path = urlparse.urlunparse(('','', path, params, query, fragment))
        logger.debug('making %s request to %s for %s.' % (httpVerb,
                                                          host, purge_path))
        conn.putrequest(httpVerb, purge_path, skip_accept_encoding=True)
        conn.endheaders()
        resp = conn.getresponse()

        xcache = resp.getheader('x-cache', '')
        xerror = ''
        for header in self.errorHeaders:
            xerror = resp.getheader(header, '')
            if xerror:
                # Break on first found.
                break
        resp.read()
        logger.debug("%s of %s: %s %s", httpVerb, url, resp.status, resp.reason)
        return resp, xcache, xerror
