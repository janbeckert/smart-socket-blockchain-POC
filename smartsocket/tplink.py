#!/usr/bin/env python3
from pyHS100 import SmartPlug
from pyHS100 import Discover

import json
import hashlib
import requests
import time
import argparse
import sys

def reportConsumption(plug, plugId, APIbase):
    pluginfo = json.loads(str(json.dumps(plug.get_emeter_realtime())))


    if(pluginfo["power"] > 5):
        print("Plug is consuming..")

        url = APIbase + "ReportConsumption"
        data = {
          "$class": "org.example.basic.ReportConsumption",
          "plug": "resource:org.example.basic.SmartPlug#" + plugId,
          "amount": "3"
        }
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(url, data=data_json, headers=headers)
    else:
        print("Plug is not consuming..")

    return False


def isCheap(n):
    return n % 8 == 3


def publishBonus(n, supplierId, APIbase):
    print("Publishing Bonus of " + str(n) + " EuroCent...")

    url = APIbase + "CreateBonus"
    data = {
      "$class": "org.example.basic.CreateBonus",
      "generate": "org.example.basic.EnergySupplier#" + supplierId,
      "euroCent": str(n)
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, data=data_json, headers=headers)


    return False


def updateBalance(plugId, APIbase):
    print("Updating balance..")

    url = APIbase + "UpdateBalance"
    data = {
      "$class": "org.example.basic.UpdateBalance",
      "plug": "resource:org.example.basic.SmartPlug#" + plugId
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, data=data_json, headers=headers)


    return False



parser = argparse.ArgumentParser(description='Run smart socket demo process',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--ip', dest='PLUG_IP', required=False, default=argparse.SUPPRESS,
                    help='ip address of the H110 compatible smart socket. If no ip is given, the tool will try to discover sockets and will use the first one found.')
parser.add_argument('--supplier', dest='SUPPLIER_ID', required=True, default=argparse.SUPPRESS,
                    help='EnergySupplier id')
parser.add_argument('--plug', dest='PLUG_ID', required=True, default=argparse.SUPPRESS,
                    help='Plug id')
parser.add_argument('--api-base', dest='APIbase', default='http://localhost:3000/api/',
                    help='Base URI of the hyperledger composer REST api.')

args = parser.parse_args()

if(args.PLUG_IP is None):
    print("No device ip given, discover new sockets..")
    plug = None
    for dev in Discover.discover().values():
        plug = dev
        print("Found a device: " + plug.host)
    if(plug is None):
        print("No device found.")
        sys.exit()
else:
    plug = SmartPlug(args.PLUG_IP)


n = 0

while True:
    n = n +1
    time.sleep(5)
    reportConsumption(plug, args.PLUG_ID)
    if(isCheap(n)):
        publishBonus(4, args.SUPPLIER_ID)
        plug.turn_on()
    else:
        plug.turn_off()
    if(n % 8 == 6):
        updateBalance(args.PLUG_ID)


