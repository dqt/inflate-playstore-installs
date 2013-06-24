from jnius import autoclass
from time import sleep
import sys
import argparse
import logging
from copy import deepcopy


x = logging.getLogger("log")
x.setLevel(logging.DEBUG)

h1 = logging.FileHandler("gplaydl.log")
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)

h2 = logging.StreamHandler()
h2.setLevel(logging.DEBUG)
f2 = logging.Formatter("%(levelname)s: %(message)s")
h2.setFormatter(f2)
x.addHandler(h2)

global x


def openAccounts(filename):
    acctDetails = {}
    accounts = []

    x.info("Opening %s", filename)

    try:
        acctlist = [line.strip() for line in open(filename)]
        x.info("%s Opened Successfully", filename)
    except Exception, err:
        x.exception(err)
        x.exception("Unable to Open %s", filename)
        x.exception("Program Will Exit\n\n")
        sys.exit(1)

    x.info("Parsing %s", filename)
    for acct in acctlist:
        try:
            lineList = acct.split(':')
        except Exception, err:
            x.exception(err)
            x.exception("Failed To Parse Accounts! Check Format")
            x.exception("Program Will Exit\n\n")
            sys.exit(1)
        try:
            if (len(lineList) == 2):
                acctDetails = {"username": lineList[0], "password": lineList[1]}
                accounts.append(deepcopy(acctDetails))
            else:
                x.exception("Failed To Parse Accounts")
                x.exception("Program Will Exit\n\n")
                sys.exit(1)
        except:
            x.exception("Failed To Parse Accounts! IDK")
            x.exception("Program Will Exit\n\n")
            sys.exit(1)
    numberOfAccts = len(accounts)
    x.info("%d Accounts Parsed Successfully", numberOfAccts)
    return accounts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--accounts", help="file containing accounts, format--> email:pass",
                        type=str)
    parser.add_argument("-adb", "--adb", help="location of ADB: /home/user/adt-bundle/sdk/platform-tools/adb",
                        type=str)
    parser.add_argument("-u", "--uri", help="application to install: market://details?id=com.my.app",
                        type=str)
    args = parser.parse_args()

    acctfile = args.accounts
    adbloc = args.adb
    marketapp = args.uri

    x.info('Application started')

    accounts = openAccounts(acctfile)

    ADB_LOCATION = str(adbloc)
    AndroidDebugBridge = autoclass('com.android.ddmlib.AndroidDebugBridge')
    AndroidDebugBridge.init(False)
    bridge = AndroidDebugBridge.createBridge(ADB_LOCATION, False)
    sleep(2)
    device = bridge.getDevices()[0]
    propsmap = device.getProperties()
    propskeys = propsmap.keySet().toArray()
    properties = dict(zip(propsmap.keySet().toArray(), propsmap.values().toArray()))
    import pprint;pprint.pprint(properties)

    AdbChimpDevice = autoclass('com.android.chimpchat.adb.AdbChimpDevice')
    chimpdevice  = AdbChimpDevice(device)
    ArrayList = autoclass('java.util.ArrayList')
    HashMap = autoclass('java.util.HashMap')

    uri        = str(marketapp)
    action     = "android.intent.action.VIEW"
    data       = None
    mime_type  = None
    categories = ArrayList()
    extras     = HashMap()
    component  = None
    flags      = 0

    for account in accounts:
        x.info('Trying--> %s:' % account['username'] + '%s ' % account['password'])
        try:
            x.info('Opening market...')
            chimpdevice.startActivity(uri, action, data, mime_type, categories, extras, component, flags)
            chimpmanager = chimpdevice.getManager()
            sleep(5)
            x.info('Logging in...')
            chimpmanager.touch(357, 986)
            sleep(5)
            chimpmanager.type(account['username'])
            sleep(5)
            chimpmanager.touch(202, 412)
            chimpmanager.type(account['password'])
            sleep(5)
            chimpmanager.touch(662, 1135)
            sleep(5)
            chimpmanager.touch(496, 864)
            x.info('Sleeping for 25 seconds...')
            sleep(25)
            x.info('Post login nonsense...')
            chimpmanager.touch(349, 1101)
            sleep(5)
            chimpmanager.touch(86, 580)
            sleep(5)
            chimpmanager.touch(624, 1104)
            x.info('Sleeping for 18 seconds...')
            sleep(18)
            x.info('Installing app...')
            chimpmanager.touch(582, 310)
            sleep(5)
            chimpmanager.touch(564, 885)
            x.info('Sleeping for 15 seconds...')
            sleep(15)
            x.info('+1ing the app')
            chimpmanager.touch(58, 858)
            x.info('Uninstalling app...')
            sleep(7)
            chimpmanager.touch(612, 334)
            sleep(7)
            chimpmanager.touch(485, 717)
            sleep(10)
            x.info('Clearing account from phone...')
            chimpmanager.touch(363, 1245)           # Home
            sleep(5)
            chimpmanager.touch(95, 141)           # Top left delAcct
            sleep(5)
            chimpmanager.touch(379, 186)
            sleep(5)
            chimpmanager.touch(367, 1232)
            sleep(5)

        except Exception, err:
            x.exception('Something went wrong:')
            x.exception(err)
            x.exception('Trying next account')


if __name__ == '__main__':
    main()
