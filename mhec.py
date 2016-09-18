# Demo MicroPython Class for HTTP Event Collector of Splunk Enterprise 6.4.x
# Version 0.1
# Support JSON, RAW data inputs and Indexer acknowledgment
# Reference: http://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector
# Disclaimer: This is not an official Splunk solution and with no liability. Use at your own risk.
# For feedback and bug report, please send to jyung@splunk.com

import time
import json
import ubinascii
import mhttp
import network

class BadRequest(Exception):
    pass

class GeneralFailure(Exception):
    pass

class hec(object):
    class BadRequest(BadRequest):
        pass

    class GeneralFailure(GeneralFailure):
        pass

    def __init__(self, indexer, port, token):
        self.indexer = indexer
        self.port = port
        self.token = token
        self.host = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        self.guid = "666a7b4b-a5b5-42b0-bf0f-3c86fa0a1b85"
        self.http = "http"

    def __submit(self, eventData):
        hecHeader = 'User-Agent: MicroPython\r\nAuthorization: Splunk %s\r\nX-Splunk-Request-Channel: %s'
        try:
            h = mhttp.http()
            head = hecHeader % (self.token, self.guid)
            status = h.open(self.url,data=eventData,header=head)
            if status == "200":
                resp = h.read()
                try:
                    respJ = json.loads(resp);
                    return respJ["ackId"]
                except KeyError:
                    return -1
            elif status == "400":
                raise BadRequest
            else:
                raise GeneralFailure
        except mhttp.InvalidHost:
            raise GeneralFailure
        except mhttp.ConnectionFailed:
            raise GeneralFailure
        except mhttp.InvalidPort:
            raise GeneralFailure

    def __queryAck(self, ackId):
        hecHeader = 'User-Agent: MicroPython\r\nAuthorization: Splunk %s\r\nX-Splunk-Request-Channel: %s'
        urlAck = self.http+"://"+self.indexer+":"+self.port+"/services/collector/ack?channel="+self.guid
        try:
            h = mhttp.http()
            head = hecHeader % (self.token, self.guid)
            status = h.open(urlAck,data=json.dumps(ackId),header=head)
            if status == "200":
                resp = h.read()
                return resp
            elif status == "400":
                raise BadRequest
            else:
                raise GeneralFailure
        except mhttp.InvalidHost:
            raise GeneralFailure
        except mhttp.ConnectionFailed:
            raise GeneralFailure
        except mhttp.InvalidPort:
            raise GeneralFailure

    def setIndexer(self, indexer):
        self.indexer = indexer

    def setIndexerPort(self, port):
        self.port = port

    def setToken(self, token):
        self.token = token

    def setHost(self, host):
        self.host = host

    def setGUID(self, guid):
        self.guid = guid

    def queryAck(self, ackId):
        return self.__queryAck(ackId)

class hecJson(hec):
    def __init__(self, indexer, port, token):
        hec.__init__(self, indexer, port, token)

    def submit(self, sourcetype, source, eventData):
        self.url = self.http+"://"+self.indexer+":"+str(self.port)+"/services/collector"
        event={}
        event["time"]=int(time.time())+946684800
        event["host"]=self.host
        event["source"]=source
        event["sourcetype"]=sourcetype
        event["event"]=eventData
        return super(hecJson,self).__submit(json.dumps(event))

class hecRaw(hec):

    def __init__(self, indexer, port, token):
        hec.__init__(self, indexer, port, token)

    def submit(self, eventData):
        self.url = self.http+"://"+self.indexer+":"+str(self.port)+"/services/collector/raw"
        return super(hecRaw,self).__submit(str(int(time.time())+946684800)+" "+eventData)
