"""
<plugin key="BBMagic" name="BBMagic BLE" author="z1mEk" version="1.0.0" wikilink="" externallink="http://bbmagic.net/">
    <description>

    </description>
    <params>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

from bbm_class import BBMagic
from time import sleep

class BasePlugin:
 
    bbm = BBMagic()
    
    def createDevices(self, bjData):
        Domoticz.Log("Check and create devices")
        device_type = bjData['device_type']
        mac = bjData['mac']
    
    def scanBBMagicDevices(self):
        Domoticz.Log("Scan BBMagic devices")
        bjData = bbm.bbm_bt_read_json()
        result = bjData['result']
        if result > 0:
            createDevices(bjData)
        elif result == 0:
            Domotic.Log("no bt data arrived")
        elif result == -1:
            Domoticz.Log("user break (ctrl+C)")
        elif result == -2:
            Domoticz.Log("data red ; not HCI event pocket")
        elif result == -4:
            Domoticz.Log("red HCI event pocket ; not LE Advertising Report event")
        elif result == -6:
            Domoticz.Log("red HCI event pocket LE Advertising Report event ; not Manufacturer specific data")
        elif result == -9:
            Domoticz.Log("reserved for: wrong Manufacturer ID")
        elif result == -10:
            Domoticz.Log("authentication error")
        elif result == -12:
            Domoticz.Log("other error")
            
    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        Domoticz.Debug("onStart called")
        i = bbm.bbm_bt_lib_version()
        Domoticz.Log("BBMagic library version is {0}".format(i))
        if i > 102:
            i = bbm.bbm_bt_lib_open(17)
            if i == 0:
                Domoticz.Log("bbm_bt_lib_open: OK")
            else:
                Domoticz.Log("bbm_bt_lib_open: Some errors occured")
        else:
            Domoticz.Log("Incompatibile bmmagic_lib {}".format(i))
        
    def onStop(self):
        Domoticz.Log("onStop called")
        i = bbm.bbm_bt_close()
        if i == 0:
            Domoticz.Log("bbm_bt_lib_close: OK")
        else:
            Domoticz.Log("bbm_bt_lib_close: Some errors occured")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called. Status: " + str(Status))

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))

    def onNotification(self, Data):
        Domoticz.Debug("onNotification: " + str(Data))

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called. Connected: " + str(self.isConnected))
        scanBBMagicDevices(self)

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, status, extra):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Data):
    global _plugin
    _plugin.onNotification(Data)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != str(sValue)):
            Domoticz.Log("Update " + str(Devices[Unit].nValue) + " -> " + str(nValue)+",'" + Devices[Unit].sValue + "' => '"+str(sValue)+"' ("+Devices[Unit].Name+")")
            Devices[Unit].Update(nValue, str(sValue))
    return

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device DeviceID:  " + str(Devices[x].DeviceID))
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
return
