class watchdataclass(object):
    scopedata = {}
    scopelog = []
    scopeitem = {}

    def __init__(self):
        print("init of watch data class")

        # urldata = "url1"
        # contentdata = "content"
        # responsetime = "1111"
        # timefreq = "1"
        # result = "ok"
        # self.scopeitem['url'] = urldata
        # self.scopeitem['keyword'] = contentdata
        # self.scopeitem['responcetime'] = responsetime
        # self.scopeitem['timefreq'] = timefreq
        # self.scopeitem['result'] = result
        #
        # print(self.scopeitem)
        # print(self.scopedata)
        # print(self.scopedata)
        #
        # self.scopedata[urldata] = self.scopeitem
        # self.scopelog.append(self.scopeitem)
        # print(self.scopedata[urldata])
        # print("log   ")
        # print(self.scopelog)
        #
        # urldata = "url2"
        # contentdata = "con2"
        # responsetime = "222"
        # timefreq = "2"
        # result = "FAIL"
        # self.scopeitem['url'] = urldata
        # self.scopeitem['keyword'] = contentdata
        # self.scopeitem['responcetime'] = responsetime
        # self.scopeitem['timefreq'] = timefreq
        # self.scopeitem['result'] = result
        #
        # print(self.scopeitem)
        # self.scopedata[urldata] = self.scopeitem
        # self.scopelog.append(self.scopeitem)
        # print(self.scopelog)

        return

    def watchdata(self):
        return

    def cleandata(self):
        watchdataclass.scopedata = {}
        watchdataclass.scopelog = []
        watchdataclass.scopeitem = {}
        return

    def findduplicatesession(self, currentsessionid):
        for existingsessionid in watchdataclass.scopedata.keys():
            if existingsessionid == currentsessionid:
                return 1  # session already exist
        return 0  # session doesnt exist
