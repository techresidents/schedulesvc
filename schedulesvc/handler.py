import logging

from trpycore.thread.util import join
from trsvcscore.service.handler.service import ServiceHandler
from trschedulesvc.gen import TScheduleService

import settings
from scheduler import ChatScheduler

class ScheduleServiceHandler(TScheduleService.Iface, ServiceHandler):
    def __init__(self, service):
        super(ScheduleServiceHandler, self).__init__(
                service,
                zookeeper_hosts=settings.ZOOKEEPER_HOSTS,
                database_connection=settings.DATABASE_CONNECTION)

        self.log = logging.getLogger("%s.%s" % (__name__, ScheduleServiceHandler.__name__))

        #create scheduler which does the real work
        self.scheduler = ChatScheduler(
                settings.SCHEDULER_THREADS,
                self.get_database_session,
                settings.SCHEDULER_POLL_SECONDS)
    
    def start(self):
        """Start handler."""
        super(ScheduleServiceHandler, self).start()
        self.scheduler.start()

    
    def stop(self):
        """Stop handler."""
        self.scheduler.stop()
        super(ScheduleServiceHandler, self).stop()

    def join(self, timeout=None):
        """Join handler."""
        join([self.scheduler, super(ScheduleServiceHandler, self)], timeout)

    def reinitialize(self, requestContext):
        """Reinitialize - nothing to do."""
        pass
