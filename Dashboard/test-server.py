import sys
import logging
import time

from networktables import NetworkTables, NetworkTable

NetworkTables.setClientMode()
NetworkTables.initialize("localhost")

table = NetworkTables.getTable("SmartDashboard")

i = 0
while True:
    table.putNumber("index", i)
    i += 1
    time.sleep(1)
