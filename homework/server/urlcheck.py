from contentscheck import contentscheckclass
import threading
import time
import datetime
import requests
import null
from watch import watchdataclass


class urlcheckclass(object):
    def __init__(self, sessionid, urlsplit, parametercount, timefreq):
        print("url check func")
        print("url   " + urlsplit[0])
        self.sessionid = sessionid
        if parametercount != 1:
            print("content    " + urlsplit[1])
        print("timefreq   " + timefreq)

        self.nextcheck = time.time()
        self.url = urlsplit[0]
        self.timefreq = float(timefreq)
        if parametercount == 2:
            self.content = urlsplit[1]
        else:
            self.content = null

        return

    def watchdog(self):

        urlcheckclass.urlcheckthreadmanage(self)
        self.nextcheck += self.timefreq

        # reference https://stackoverflow.com/a/18180189/2808371
        if self.watchdogflag == 1:
            watchdataclass.scopeitem['checkfreq'] = self.timefreq
            threading.Timer(self.nextcheck - time.time(), self.watchdog).start()
        # class threading.Timer(interval, function, args=None, kwargs=None)

        return "url check call back"

    def urlcheckthreadmanage(self):
        # print("urlcheck func")

        threads = []

        t = threading.Thread(target=self.urlcheckexecute, args=(self.sessionid, self.url, self.content))
        threads.append(t)
        t.start()
        return

    def urlcheckexecute(self, sessionid, url, content):
        response = self.make_request(url)

        if not response:
            # print("connection error")
            watchdataclass.scopeitem['time'] = str(datetime.datetime.now())
            watchdataclass.scopeitem['url'] = url
            watchdataclass.scopeitem['responcetime'] = "null"
            watchdataclass.scopeitem['keyword'] = "null"

            watchdataclass.scopedata[sessionid] = watchdataclass.scopeitem.copy()
            watchdataclass.scopelog.append(watchdataclass.scopeitem.copy())
            print(watchdataclass.scopedata[sessionid])
            return
        response_time = str(response.elapsed.total_seconds())
        # print("url: " + url +"   response time: "+response_time)

        if content != null:
            # contentscheckclass.contentscheck(content) #this is not in use
            self.contentcheck(response, content)
            watchdataclass.scopeitem['keyword'] = content
        else:
            # print("no content for search")
            watchdataclass.scopeitem['keyword'] = "null"
            watchdataclass.scopeitem['result'] = "website up but keyword NOT defined"

            # put the logs
        watchdataclass.scopeitem['time'] = str(datetime.datetime.now())
        watchdataclass.scopeitem['url'] = url
        watchdataclass.scopeitem['responcetime'] = response_time
        watchdataclass.scopedata[sessionid] = watchdataclass.scopeitem.copy()
        watchdataclass.scopelog.append(watchdataclass.scopeitem.copy())
        print(watchdataclass.scopeitem)

    @staticmethod
    def make_request(url):

        try:
            response = requests.get("http://" + url)
        except requests.exceptions.Timeout:
            # print("time out")
            watchdataclass.scopeitem['result'] = "website TIMEOUT"
        except requests.exceptions.TooManyRedirects:
            # print("too many redirects")
            watchdataclass.scopeitem['result'] = "website TOO MANY REDIRECTINO"
        except requests.ConnectionError as e:
            # print("connection error")
            watchdataclass.scopeitem['result'] = "website DOWN"

            # print(e)
            return
        except requests.exceptions.RequestException as e:
            print(e)
            # catastrophic error.
            #     raise SystemExit(e)
            return e
        return response

    @staticmethod
    def contentcheck(response, content):
        contentresult = content in response.text
        if contentresult == 1:
            # print("keyword found" + "  " + str(response.elapsed.total_seconds()))
            watchdataclass.scopeitem['result'] = "website up and keyword FOUND"
        else:
            # print("keyword NOT found but url is valid" + "  " + str(response.elapsed.total_seconds()))  # return result
            watchdataclass.scopeitem['result'] = "website up and keyword NOT found"
        return
