#!/usr/bin/env python

import logging
import logging.config
import signal
import sys
import gevent

import settings

from trpycore.process.pid import pidfile, PidFileException
from trsvcscore.service_gevent.base import GService
from trschedulesvc.gen import TScheduleService

from handler import ScheduleServiceHandler


class ScheduleService(GService):
    def __init__(self):

        handler = ScheduleServiceHandler()

        super(ScheduleService, self).__init__(
                name=settings.SERVICE,
                interface=settings.SERVER_INTERFACE,
                port=settings.SERVER_PORT,
                handler=handler,
                processor=TScheduleService.Processor(handler))
 
def main(argv):
    try:
        with pidfile(settings.SERVICE_PID_FILE, create_directory=True):

            #Configure logger
            logging.config.dictConfig(settings.LOGGING)
            
            #Create service
            service = ScheduleService()
            
            def sigterm_handler():
                service.stop()

            gevent.signal(signal.SIGTERM, sigterm_handler);

            service.start()
            service.join()
    
    except PidFileException as error:
        logging.error("Service is already running: %s" % str(error))

    except KeyboardInterrupt:
        service.stop()
        service.join()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
