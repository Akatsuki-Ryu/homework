from configcheck import configcheckclass


class configloadclass(object):
    def __init__(self):
        print("init of config load class")
        return

    def configload(self, urlval, timefreq):
        # todo here we can control the input and filter out invalid input
        print("config load func    " + urlval)
        configcheckclass.configcheck(self, urlval, timefreq)
        return "config load call back"
