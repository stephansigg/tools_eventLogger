#!/usr/bin/python
# -*- coding: utf-8 -*-

##
## Mario: Demo for PyMouse mouse capturing.
## needs: PyMouse (https://github.com/pepijndevos/PyMouse) *
## needs: sudo apt-get install python-xlib
##
## Note: this library can also move and click the mouse.
##          And query its position.
##
## *) for mouse wheel support unix.py has to be patched!
##    (there seems to be good solution on github but waiting for acceptance (since 2 years..))
##    Quick fix: [in class PyMouseEvent(PyMouseEventMeta)]
##       _BUTTONS = (0, 1, 3, 2, 4, 5, 0)   ## with mouse wheel
##       self._BUTTONS[event.detail]  ## (in handler..)
##

from pymouse import PyMouse
from pymouse import PyMouseEvent
#import time

import sys
from signal import signal, SIGINT, SIGTERM

import logging2
import datetime


## release mouse if we got killed
def emergency_stop(signum, frame):
    print "Got killed! Releasing mouse."
    regular_quit()
    sys.exit()
signal(SIGINT, emergency_stop)
signal(SIGTERM, emergency_stop)


class event(PyMouseEvent):
    DEBUG = False
    BUTTONS = ("INVALID", "LEFT", "RIGHT", "MIDDLE", "scroll_up", "scroll_down")
    
    def __init__(self):
        super(event, self).__init__()
        
        self.logger = logging2.Logger()

    def move(self, x, y):
        pass

    def click(self, x, y, button, press):
        ## debug output
        if ( self.DEBUG ):
            if press:
                print 'press\t(' + str(x) + ', ' + str(y) + ')', self.BUTTONS[button]
            else:
                print 'release\t(' + str(x) + ', ' + str(y) + ')', self.BUTTONS[button]
                print

        ## only log mouse down, at the moment
        if ( press ):
            self.logger.log(self.BUTTONS[button])
            
    def close_and_save(self, path):
        self.stop()
        self.logger.save(path)




## stop monitoring, release the mouse, close logger
def regular_quit(path = None):
    e.close_and_save(path)


### main ###
if __name__ == "__main__":
    e = event()
    e.capture = True  ## True: mouse can't click anything, False: mouse acts normal
    e.daemon = False
    e.start()

    print
    print "Logger started. Press [Enter] when finished."

    ## quit on enter
    x = raw_input()
    regular_quit("/tmp/mouse.csv")  ## TODO customizeable ?
#    regular_quit()

    print "bye."

