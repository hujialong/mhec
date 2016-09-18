# Usage Example: event is submitted in JSON format, temperature in Celsius

import mhec
import mMCP9808
import time

hecSrv = '192.168.10.36'
hecSPort = 8088
hecToken = 'C33F175C-F01E-4F8C-838B-B3DE26B04AD8'

sensor0 = mMCP9808.mMCP9808()
if sensor0.start():
    sourcetype = 'MCP9808'
    while True:
        event = {}
        event["Temperature"] = sensor0.getTemp()
        hec0 = mhec.hecJson(hecSrv, hecSPort, hecToken)
        try:
            resp = hec0.submit(sourcetype, "mMCP9808.py", event)
            print(resp)
        except mhec.BadRequest:
            pass
        except mhec.GeneralFailure:
            pass
        time.sleep(5)
