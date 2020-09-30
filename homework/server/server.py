from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask import render_template
import requests
from time import sleep
import threading

from configload import configloadclass
from urlcheck import urlcheckclass
from configcheck import configcheckclass
from watch import watchdataclass

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
api = Api(app)

CORS(app)

# this is a global scope
scopedata = []
scoperesult = []

countingval = 100


# this is a global method
def waitonesec(message):
    scopedata.append("waited")
    global countingval
    print(countingval)
    countingval = countingval + 1
    return message


# first prototype , not in use
def checkurl(echoval, timefreq):
    for loopi in range(0, 1):
        print("======================================================")

        # input control
        if echoval.find("&&") != -1:
            parametercount = 2
            searchurl = echoval.split("&&")
            print(searchurl[0])
            print(searchurl[1])
        else:
            print("only one parameter")
            parametercount = 1
            searchurl = echoval.split("&&")

        # print(echoval[0:8])
        # if echoval[0:8] == "https://":
        #     print(echoval[0:3])
        #     print("abcd in the front")
        #     return "abcd in the front"

        # urlcheck
        try:
            responce = requests.get("http://" + searchurl[0])
        except requests.exceptions.Timeout:
            print("time out")
        except requests.exceptions.TooManyRedirects:
            print("too many redirects")
        except requests.ConnectionError as e:
            print("connection error")
            print(e)
            scoperesult.append("url NOT found")
            return scoperesult
        except requests.exceptions.RequestException as e:
            print(e)
            # catastrophic error. bail.
            #     raise SystemExit(e)
            return e

        # print(responce.status_code)

        if (responce.status_code == 200):
            # print(responce.status_code)
            print("url found")
            if parametercount != 1:
                keyword = searchurl[1] in responce.text
                if keyword == 1:
                    scoperesult.append("keyword found" + "  " + str(responce.elapsed.total_seconds()))
                    # return result
                else:
                    scoperesult.append(
                        "keyword NOT found but url is valid" + "  " + str(responce.elapsed.total_seconds()))
                    # return result
            else:
                scoperesult.append("URL found , but no keyward " + "  " + str(responce.elapsed.total_seconds()))
        # print(responce.text)

        # search sting

        # print(echoval)
        # result.append("wtf" + "  " + str(responce.elapsed.total_seconds()))
        sleep(timefreq)
    return scoperesult


@app.route("/")
def hello():
    # return "hello world"
    return render_template('result.html')


class echologic(Resource):
    def get(self, echoval):
        print(scoperesult)
        result = checkurl(echoval, 1)

        return render_template('result.html', data=scoperesult)
        # return result
        # return str(countingval)


class echologicfreq(Resource):
    def get(self, echoval, freq):
        time = int(freq)
        result = checkurl(echoval, time)
        return result


class inputdata(Resource):
    def get(self, checkval):
        # todo check against to the current task list ,if doenst exist , then create new scan .
        if watchdataclass.findduplicatesession(self, checkval):
            return (checkval + "already exist")
        urlcheckclass.watchdogflag = 1
        configloadclass.configload(self, checkval, "5")
        return (checkval + "has been watched at frequency of 5 sec")


class inputdatawithfreq(Resource):
    def get(self, checkval, freq):
        # todo check against to the current task list ,if doenst exist , then create new scan .
        if watchdataclass.findduplicatesession(self, checkval):
            return (checkval + "already exist")
        urlcheckclass.watchdogflag = 1
        if configcheckclass.freqcheck(freq) != 0:
            return "time frequency is incorrect"
        configloadclass.configload(self, checkval, freq)
        return (checkval + "has been watched at frequency of " + freq + " sec")


class killwatchdog(Resource):
    def get(self):
        urlcheckclass.watchdogflag = 0
        watchdataclass.cleandata(self)
        return jsonify("watch dog is killed and data is also restored ")


class watchdog(Resource):
    def get(self):
        # print(watchdataclass.scopedata)
        # result = json.dumps(watchdataclass.scopedata) #parsing problem , not in use
        return jsonify(watchdataclass.scopedata)


class log(Resource):
    def get(self):
        watchdataclass()  # this is not in use
        # print(watchdataclass.scopelog)
        # result = json.dumps(watchdataclass.scopelog)
        return jsonify(watchdataclass.scopelog)


api.add_resource(echologic, '/echo/<echoval>')
api.add_resource(echologicfreq, '/echo/<echoval>/<freq>')
api.add_resource(inputdata, '/input/<checkval>')
api.add_resource(inputdatawithfreq, '/input/<checkval>/<freq>')
api.add_resource(killwatchdog, '/kill')
api.add_resource(watchdog, '/watch')
api.add_resource(log, '/log')


def main():
    print("=====================================================================start")
    # configloadclass.configload("checkvalfrommain", 1)
    # urlcheckclass.urlcheck()
    # print(configloadclass.configload())
    # print(urlcheckclass.urlcheck())
    # watchdataclass(scoperesult)


if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=5111, debug=True)
