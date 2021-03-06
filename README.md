# Demo MicroPython Class for HTTP Event Collector of Splunk Enterprise 6.4.x
- mhec.py
- Tested on AdaFruit Feather HUZZAH with 8266 (https://www.adafruit.com/products/2821) running MicroPython esp8266-20160909-v1.8.4.bin (http://micropython.org/download/#esp8266)
- Support JSON, RAW data inputs and Indexer acknowledgment
- Reference: http://docs.splunk.com/Documentation/Splunk/6.4.2/Data/UsetheHTTPEventCollector
- Disclaimer: This is not an official Splunk solution and with no liability. Use at your own risk.
- For feedback and bug report, please send to jyung@splunk.com
- Other supporting files
  - mhttp.py: Demo class for HTTP POST, SSL is not supported.
  - mMCP9808.py: Demo class for I2C temperature sensor breakout, https://www.adafruit.com/products/1782 
  - hecJsontest.py: Usage example

# Usage
**First step**. Import the Class
```python
  import mhec
```

**Option 1**. JSON Data payload
```python
  mhec.hecJson(String: indexer ip address,String: port,String: token)
  mhec.submit(String: sourcetype,String: source,Json: event)
```
e.g.
```python
  myHEC = mhec.hecJson("192.168.10.8","8088","75475867-EE4F-4357-BBA3-03F1D66F3697")
  myHEC.submit("10dof","sensorData.py",eventData)
```

**Option 2**. RAW Data payload
```python
  hec.mhecRaw(String: index ip address,String: port,String: token)
  hec.submit(String: raw event)
```
e.g.
```python
  myHEC = mhec.hecRaw("192.168.10.8","8088","75475867-EE4F-4357-BBA3-03F1D66F3697")
  myHec.submit("Raw event data example")
````

**Optional Indexer Acknowledgment**: support both hecRaw and hecJson
```python
  ackId = myHEC.submit("10dof","sensorData.py",eventData)
```
- ackId: -1 indicates Indexer Acknowledgment is disabled on the indexer. Number > 0 is the acknowledgment number of the transfer

To query if the payload of specific acknowledgment number is indexed, e.g.
```python
  respRack = hec0.queryAck([5581,5582])
```
- ackEvent: an array of acknowledgment number
- respRack: a json object containing the result of the acknowledgment number status

For details, please refer to [Splunk Documentation](http://dev.splunk.com/view/event-collector/SP-CAAAE8X)

* *Note: Event timestamp is the time when the event is submitted, not the time it is received by Indexer.*

**Other supporting methods**
```python
  setIndexer(String: indexer ip address)
```

```python
  setIndexerPort(String: indexer port)
```

```python
  setGUID(String: guid)
```
* *Note: the class come with a fixed, default GUID. It's recommended to assign new GUID for a dedicated data channel*
```python
  setHost(String: Value of the meta field 'host')
```
* *Note: default is the mac address*
```python
  setToken(String: Token of the HEC channel)
```
