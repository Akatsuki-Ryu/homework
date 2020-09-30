from urlcheck import urlcheckclass
from watch import watchdataclass


class configcheckclass(object):
    def __init__(self):
        print("init of config check class")
        self.sessionid = 0
        return

    def configcheck(self, urlval, timefreq):
        print("config check func")
        self.sessionid = urlval
        # input control
        if urlval.find("&&") != -1:
            parametercount = 2
            urlvalsplit = urlval.split("&&")
            print("the url is    " + urlvalsplit[0])
            print("search is     " + urlvalsplit[1])
            urlcheckclass(urlval, urlvalsplit, parametercount, timefreq).watchdog()
        else:
            print("only one parameter")
            parametercount = 1
            urlvalsplit = urlval.split("&&")
            print(urlvalsplit[0])
            urlcheckclass(urlval, urlvalsplit, parametercount, timefreq).watchdog()
        return "config check func call back"

    def freqcheck(freq):
        if freq.isnumeric():
            if float(freq) < 0.2:
                return 1
            return 0
        return 1
