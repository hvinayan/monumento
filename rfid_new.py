from pubnub import Pubnub
pubnub = Pubnub(publish_key='pub-c-0bb87cba-798a-4074-a4c4-ef877921331e', subscribe_key='sub-c-7a3fc736-ed8c-11e5-8f88-0619f8945a4f')

def callback(message):
     print message

def _callback(message, channel):
  print "S :", message

def _error(message):
    print(message)

pubnub.subscribe(channels="monument_channel", callback=_callback, error=_error)

import serial
ser = serial.Serial('/dev/cu.SLAB_USBtoUART')
# ser.timeout = 1
while True:
    rfid = ser.read(12)
    print rfid
    pubnub.publish('monument_channel', "[{latlng: [28.617748,77.195100],marker: me},{latlng: [28.6177,77.2011],marker: them},{latlng: [28.6172,77.1910],marker: them},{latlng: [28.617748,77.195100],marker: them},{latlng: [28.6174,77.19544],marker: them},{latlng: [28.617467,77.2022],marker: them}];", callback=callback, error=callback)
