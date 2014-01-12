# -*- coding: utf-8 -*-

import time
import datetime

## struct: Event
class Event(object):
    def __init__(self):
        self.start = None
        self.end = None
        self.payload = None
    
    def __str__(self):
        return str(self.start) + " - " + str(self.end) + ":\t" + str(self.payload)
        
    
## Logger class
class Logger(object):
    DEBUG = True
    
    def __init__(self):
        self.events = list()
        self.cur_event = None


    ## end of last event, if any
    def fin_current(self, t=None):
        # fin now (or at given time t, if any)
        if ( not t ):
            #t = time.time()
            t = datetime.datetime.today().isoformat()
    
        # * fin *
        if ( self.cur_event ):
            self.cur_event.end = t
            self.cur_event = None


    ## log new event
    def log(self, payload):
        #t = time.time()
        t = datetime.datetime.today().isoformat()
        
        ## end of last event, if any    
        self.fin_current(t)
        
        ## begin of new one
        e = Event()
        e.start = t
        e.payload = payload
        
        ## store
        self.cur_event = e
        self.events.append(e)
        
        ## debug
        if ( self.DEBUG ):
            print "LOG:", e


    ## XXX testing close, save, sonstwas..
    def close(self):
        self.fin_current()
        
#        print
#        print "-" * 20
#        print
#        for x in self.events:
#            print x


    def save(self, path):
        # fin current
        self.fin_current()
        
        # init
        ref_time = self.events[0].start
        out = list()
        
        # write header
        out.append("Start (rel),End (rel),Start (abs),End (abs),Label\n")
        
        
        # create csv output
        for x in self.events:
            line = list()
            
            # rel times
            line.append(str(x.start - ref_time))
            line.append(str(x.end - ref_time))
            # abs times
            line.append(str(x.start))
            line.append(str(x.end))
            # payload
            line.append(str(x.payload))
            
            line_str = ",".join(line) + "\n"
            out.append(line_str)


        ## BRANCH: writes output into file
        if ( path ):
            f = open(path, 'w')
            f.writelines(out)
            f.close()
            
            print "Written to:", path
            
        ## BRANCH: no file given, print output on stdout
        else:
            # debug output
            for x in out:
                print x,
            print

