import logging
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, PROJECT_ROOT)

from trpycore import riak_gevent
from trpycore.riak_common.factory import RiakClientFactory
from trsvcscore.service_gevent.handler import GServiceHandler
from trsvcscore.session.riak import RiakSessionStorePool
from tridlcore.gen.ttypes import RequestContext
from trschedulesvc.gen import TScheduleService

import version
import settings


class ScheduleServiceHandler(TScheduleService.Iface, GServiceHandler):
    def __init__(self):
        super(ScheduleServiceHandler, self).__init__(
                name=settings.SERVICE,
                interface=settings.SERVER_INTERFACE,
                port=settings.SERVER_PORT,
                version=version.VERSION,
                build=version.BUILD,
                zookeeper_hosts=settings.ZOOKEEPER_HOSTS,
                database_connection=settings.DATABASE_CONNECTION)
        
        self.log = logging.getLogger("%s.%s" % (__name__, ScheduleServiceHandler.__name__))

        self.riak_client_factory = RiakClientFactory(
                host=settings.RIAK_HOST,
                port=settings.RIAK_PORT,
                transport_class=riak_gevent.RiakPbcTransport)

        self.session_store_pool = RiakSessionStorePool(
                self.riak_client_factory,
                settings.RIAK_SESSION_BUCKET,
                settings.RIAK_SESSION_POOL_SIZE)
    
    def reinitialize(self, requestContext):
        pass
