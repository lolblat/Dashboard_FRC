# TODO: add storing data inside sqlDB
import sys
import logging
import json
from networktables import NetworkTables

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

KEY_NUMBER = "NUMBER"
KEY_STRING = "STRING"
KEY_BOOLEAN = "BOOLEAN"
KEY_RAW = "RAW"
logging.basicConfig(level=logging.DEBUG)


def assignToTable(table, key, value, type=""):
    if type == "":
        table.putValue(key, value)
    elif type == KEY_NUMBER:
        table.putNumber(key, value)
    elif type == KEY_STRING:
        table.putString(key, value)
    elif type == KEY_BOOLEAN:
        table.putBoolean(key, value)
    elif type == KEY_RAW:
        table.putRaw(key, value)


def encodeToJson(dict, key="*"):
    if key == "*":
        return json.dumps(dict)
    else:
        return json.dumps({key: dict[key]})


def help():
    print("---------------------------------")
    print("|     Dashboard Program         |")
    print("| Developed for: FRC team 2630  |")
    print("|         ThunderBolts          |")
    print("|    Developer: Orr Shachaff    |")
    print("|    args: 1) TeamNumber / IP   |")
    print("---------------------------------")


def valuechanged(table, key, value, isNew):
    print("Value changed key: %s value: %s" % (key, value))
    keysDict[key] = value



def connected(b, info):
    print("Connected to ", info.remote_port)


if len(sys.argv) != 2:
    print("Not enough args")
    help()

number = sys.argv[1]
dashLocation = ""

if "." not in number:
    dashLocation = "roborio-" + number + "-frc.local"
else:
    dashLocation = number

if "localhost" == number:
    dashLocation = "localhost"

NetworkTables.setClientMode()
NetworkTables.setIPAddress(address=dashLocation)
NetworkTables.initialize()

sm = NetworkTables.getTable("SmartDashboard")

sm.addConnectionListener(connected)

keysDict = {}

for key in sm.getKeys():
    keysDict[key] = sm.getValue(key, "0")

sm.addTableListener(valuechanged)


class DashboardServer(WebSocket):
    def handleMessage(self):
        # GET - GET <key>
        # PUT - PUT <key> <value>

        req = "GET" if "GET" in self.data else "PUT" if "PUT" in self.data else ""
        if req == "":
            self.sendMessage("[ERROR] send or GET or PUT requests only")

        keyValueArray = self.data.replace("+ ", " ").split(" ")
        if req == "GET":
            if len(keyValueArray) != 2:
                self.sendMessage("[ERROR] send GET params correctly, GET <key>")
                return
            tableKey = keyValueArray[1]
            value = "{}"
            if tableKey in keysDict or tableKey == "*":
                value = encodeToJson(keysDict, tableKey)
            self.sendMessage(value)
        else:
            if len(keyValueArray) < 3 or len(keyValueArray) > 4:
                self.sendMessage("[ERROR] send PUT params correctly, PUT <key> <value> <?type?>")
                return
            putKey = keyValueArray[1]
            putValue = keyValueArray[2]
            putType = ""
            if len(keyValueArray) == 4:
                putType = keyValueArray[3]
            assignToTable(sm, putKey, putValue, putType)
            # Assign to table
            keysDict[putKey] = putValue
            print("Assigned Key: " + putKey + " Value: " + putValue)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, DashboardServer)
server.serveforever()
