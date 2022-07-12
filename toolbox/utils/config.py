import os
import socket
import urllib.request

def getUrl() -> None:
    try:
        result = urllib.request.urlopen("https://ident.me").read().decode("utf8")
    except Exception as x:
        print(type(x),x)
        result = '0.0.0.0'
        pass
    return result

class validatorToolbox:
    easyVersion = "1.5.0"
    serverHostName = socket.gethostname()
    userHomeDir = os.path.expanduser("~")
    dotenv_file = f"{userHomeDir}/.easynode.env"
    activeUserName = os.path.split(userHomeDir)[-1]
    harmonyDirPath = os.path.join(userHomeDir, "harmony")
    harmonyAppPath = os.path.join(harmonyDirPath, "harmony")
    blsKeyFile = os.path.join(harmonyDirPath, "blskey.pass")
    hmyAppPath = os.path.join(harmonyDirPath, "hmy")
    harmonyConfPath = os.path.join(harmonyDirPath, "harmony.conf")
    blskeyDirPath = os.path.join(hmyAppPath, ".hmy", "blskeys")
    hmyWalletStorePath = os.path.join(userHomeDir, ".hmy_cli", "account-keys", activeUserName)
    toolboxLocation = os.path.join(userHomeDir, "validatortoolbox")
    validatorData = os.path.join(toolboxLocation, "toolbox", "metadata", "validator.json")
    passwordPath = os.path.join(harmonyDirPath, "passphrase.txt")
    toolboxLocation = os.path.join(userHomeDir, "validatortoolbox")
    ourExternalIPAddress = getUrl()
    mainMenuRegular = os.path.join(toolboxLocation, "toolbox", "messages", "regularmenu.txt")
    mainMenuFull = os.path.join(toolboxLocation, "toolbox", "messages", "fullmenu.txt")
    rpc_endpoints = ['https://api.s0.t.hmny.io', 'https://api.harmony.one', 'https://harmony-0-rpc.gateway.pokt.network']
    rpc_endpoints_test = ['https://rpc.s0.b.hmny.io', 'https://api.s0.pops.one']
    rpc_endpoints_max_connection_retries = 10