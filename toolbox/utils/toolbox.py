import os
import shutil
import requests
import time
import dotenv
import json
import subprocess
from subprocess import Popen, PIPE, run
from ast import literal_eval
from utils.config import validatorToolbox
from os import environ
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple
from colorama import Fore, Back, Style
from pyhmy import blockchain, account
from requests.exceptions import HTTPError
from utils.library import process_command, printStars, printStarsReset, printWhiteSpace, askYesNo, return_txt, installHarmonyApp, installHmyApp, getSignPercent, loadVarFile, getWalletBalance, getRewardsBalance, stringStars
from utils.allsysinfo import allSysInfo


def collectRewards(networkCall):
    os.system(
        f"{networkCall} staking collect-rewards --delegator-addr {environ.get('VALIDATOR_WALLET')} --gas-price 100 {environ.get('PASS_SWITCH')}"
    )


def rewardsCollector() -> None:
    printStars()
    print("* Harmony ONE Rewards Collection")
    printStars()
    question = askYesNo(
        f"*\n* For your validator wallet {environ.get('VALIDATOR_WALLET')}\n* You have {getRewardsBalance(validatorToolbox.rpc_endpoints, environ.get('VALIDATOR_WALLET'))} $ONE pending.\n* Would you like to collect your rewards on the Harmony mainnet? (YES/NO) "
    )
    if question:
        collectRewards(f"{environ.get('NETWORK_0_CALL')}")
        printStars()
        print(
            Fore.GREEN + f"* mainnet rewards for {environ.get('VALIDATOR_WALLET')} have been collected." + Style.RESET_ALL
        )
        printStars()
    question = askYesNo(
        f"*\n* For your validator wallet {environ.get('VALIDATOR_WALLET')}\n* You have {getRewardsBalance(validatorToolbox.rpc_endpoints_test, environ.get('VALIDATOR_WALLET'))} $ONE pending.\n* Would you like to collect your rewards on the Harmony testnet? (YES/NO) "
    )
    if question:
        collectRewards(f"{environ.get('NETWORK_0_CALL')}")
        print()
        printStars()
        print(
            Fore.YELLOW + f"* testnet rewards for {environ.get('VALIDATOR_WALLET')} have been collected." + Style.RESET_ALL
        )
        printStars()
        print()
        input("Press ENTER to return to the main menu.")


def menuTopperRegular() -> None:
    current_epoch = getCurrentEpoch()
    sign_percentage = getSignPercent()
    os.system("clear")
    # Print Menu
    print(Style.RESET_ALL)
    printStars()
    print(
        "* "
        + Fore.GREEN
        + "validator-toolbox for Harmony ONE Validators by Easy Node   v"
        + validatorToolbox.easyVersion
        + Style.RESET_ALL
        + "   https://easynode.one *"
    )
    printStars()
    print(
        "* Your validator wallet address is: "
        + Fore.RED
        + str(environ.get("VALIDATOR_WALLET"))
        + Style.RESET_ALL
    )
    print(
        "* Server Hostname & IP:             "
        + validatorToolbox.serverHostName
        + Style.RESET_ALL
        + " - "
        + Fore.YELLOW
        + validatorToolbox.ourExternalIPAddress
        + Style.RESET_ALL
    )
    harmonyServiceStatus()
    print(
        "* Epoch Signing Percentage:         "
        + Style.BRIGHT
        + Fore.GREEN
        + Back.BLUE
        + sign_percentage
        + " %"
        + Style.RESET_ALL
    )
    print(
        "* Current disk space free: "
        + Fore.CYAN
        + f"{freeSpaceCheck(): >6}"
        + Style.RESET_ALL
        + "   Current Epoch: "
        + Fore.GREEN
        + str(current_epoch)
        + Style.RESET_ALL
    )
    printStarsReset()


def menuTopperFull() -> None:
    current_epoch = getCurrentEpoch()
    os.system("clear")
    # Print Menu
    print(Style.RESET_ALL)
    printStars()
    print(
        "* "
        + Fore.GREEN
        + "validator-toolbox for Harmony ONE Validators by Easy Node   v"
        + str(environ.get("EASY_VERSION"))
        + Style.RESET_ALL
        + "   https://easynode.one *"
    )
    printStars()
    print(
        "* Server Hostname & IP:             "
        + validatorToolbox.serverHostName
        + Style.RESET_ALL
        + " - "
        + Fore.YELLOW
        + validatorToolbox.ourExternalIPAddress
        + Style.RESET_ALL
    )
    harmonyServiceStatus()
    print(
        "* Current disk space free: "
        + Fore.CYAN
        + f"{freeSpaceCheck(): >6}"
        + Style.RESET_ALL
        + "   Current Epoch: "
        + Fore.GREEN
        + str(current_epoch)
        + Style.RESET_ALL
    )
    printStarsReset()


def menuRegular() -> None:
    menuTopperRegular()
    print(Style.RESET_ALL)
    for x in return_txt(
        validatorToolbox.mainMenuRegular
    ):
        x = x.strip()
        try:
            x = eval(x)
        except SyntaxError:
            pass
        if x:
            print(x)


def menuFull() -> None:
    menuTopperFull()
    print(Style.RESET_ALL)
    for x in return_txt(
        validatorToolbox.mainMenuFull
    ):
        x = x.strip()
        try:
            x = eval(x)
        except SyntaxError:
            pass
        if x:
            print(x)


def getWalletJSON(wallet: str) -> str:
    testOrMain = environ.get("NETWORK")
    try:
            response = requests.get(f"https://api.stake.hmny.io/networks/{testOrMain}/validators/{wallet}")
            response.raise_for_status()
            # access JSOn content
            jsonResponse = response.json()
    #        print("Entire JSON response")
    #        print(jsonResponse)
    except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'* You have not created your validator yet, try again after you add one!\n* cd ~/harmony\n* ./hmy keys recover-from-mnemonic {validatorToolbox.activeUserName} {environ.get("PASS_SWITCH")}')
            input("Press ENTER to return to the main menu.")
            return
    except Exception as err:
            print(f'Other error occurred: {err}')
            input("Press ENTER to return to the main menu.")
            return
    return(jsonResponse)


def tmiServerInfo() -> None:
    validatorWallet = environ.get('VALIDATOR_WALLET')
    jsonResponse = getWalletJSON(validatorWallet)
    for key, value in jsonResponse.items():
        print(key, ":", value)
    printStarsReset()
    input("Press ENTER to return to the main menu.")


def runFullNode() -> None:
    loadVarFile()
    menu_options = {
        # 0: finish_node,
        1: runStats,
        2: menuCheckBalance,
        3: comingSoon,
        4: comingSoon,
        5: comingSoon,
        6: comingSoon,
        7: comingSoon,
        8: menuServiceStopStart,
        9: menuServiceRestart,
        10: menuBinaryUpdates,
        11: hmyCLIUpgrade,
        12: menuUbuntuUpdates,
        13: serverDriveCheck,
        14: comingSoon,
        15: allSysInfo,
        999: menuRebootServer,
    }
    while True:
        menuFull()
        try:
            option = int(input("Enter your option: "))
        except ValueError:
                os.system("clear")
                printWhiteSpace()
                printStarsReset()
                print(
                    "* "
                    + Fore.RED
                    + "WARNING"
                    + Style.RESET_ALL
                    + ": Only numbers are possible, please try your selection on the main menu once again."
                )
                printStarsReset()
                printWhiteSpace()
                input("* Press ENTER to return to the main menu")
                runFullNode(environ.get("NODE_TYPE"))
        if option == 0:
            return finish_node()
        os.system("clear")
        menu_options[option]()


def bingoChecker():
    os.system("grep BINGO ~/harmony/latest/zerolog-harmony.log | tail -10")
    input("* Press enter to return to the main menu.")

def comingSoon():
    os.system("clear")
    printWhiteSpace()
    printStars()
    print("* This option isn't available on your system, yet!")
    printStars()
    input("* Press enter to return to the main menu.")

def runRegularNode() -> None:
    loadVarFile()
    menu_options = {
        # 0: finish_node, 
        1: runStats,
        2: menuActiveBLS,
        3: menuCheckBalance,
        4: rewardsCollector,
        5: bingoChecker,
        6: comingSoon,
        7: comingSoon,
        8: menuServiceStopStart,
        9: menuServiceRestart,
        10: menuBinaryUpdates,
        11: hmyCLIUpgrade,
        12: menuUbuntuUpdates,
        13: serverDriveCheck,
        14: tmiServerInfo,
        15: allSysInfo,
        999: menuRebootServer,
    }
    while True:
        menuRegular()
        try:
            option = int(input("Enter your option: "))
        except ValueError:
                os.system("clear")
                printWhiteSpace()
                printStarsReset()
                print(
                    "* "
                    + Fore.RED
                    + "WARNING"
                    + Style.RESET_ALL
                    + ": Only numbers are possible, please try your selection on the main menu once again."
                )
                printStarsReset()
                printWhiteSpace()
                input("* Press ENTER to return to the main menu")
                runRegularNode()
        if option == 0:
            return finish_node()
        os.system("clear")
        menu_options[option]()


def osUpgrades() -> None:
    printStars()
    upgrades = (
        "sudo apt update",
        "sudo apt upgrade -y",
        "sudo apt dist-upgrade -y",
        "sudo apt autoremove -y",
    )
    for x in upgrades:
        process_command(x)
    printStars()


def harmonyServiceStatus() -> None:
    status = subprocess.call(["systemctl", "is-active", "--quiet", "harmony"])
    if status == 0:
        print(
            "* Harmony Service is:               "
            + Fore.BLACK
            + Back.GREEN
            + "   Online  "
            + Style.RESET_ALL
        )
    else:
        print(
            "* Harmony Service is:               "
            + Fore.WHITE
            + Back.RED
            + "  *** Offline *** "
            + Style.RESET_ALL
        )


def diskFreeSpace(mountPoint: str) -> str:
    _, _, free = shutil.disk_usage(mountPoint)
    free = str(convertedUnit(free))
    return free


def freeSpaceCheck() -> str:
    ourDiskMount = get_mount_point(validatorToolbox.harmonyDirPath)
    _, _, free = shutil.disk_usage(ourDiskMount)
    free = diskFreeSpace(ourDiskMount)
    return free


def serverDriveCheck() -> None:
    if environ.get("MOUNT_POINT") is not None:
        ourDiskMount = environ.get("MOUNT_POINT")
    else:
        dotenv.set_key(validatorToolbox.dotenv_file, "MOUNT_POINT", validatorToolbox.harmonyDirPath)
        load_dotenv(validatorToolbox.dotenv_file)
        ourDiskMount = environ.get("MOUNT_POINT")
    printStarsReset()
    print("Here are all of your mount points: ")
    for part in disk_partitions():
        print(part)
    printStars()
    total, used, free = shutil.disk_usage(ourDiskMount)
    total = str(convertedUnit(total))
    used = str(convertedUnit(used))
    print(
        "Disk: "
        + str(ourDiskMount)
        + "\n"
        + freeSpaceCheck()
        + " Free\n"
        + used
        + " Used\n"
        + total
        + " Total"
    )
    printStars()
    input("Disk check complete, press ENTER to return to the main menu. ")


def disk_partitions(all=False):
    disk_ntuple = namedtuple("partition", "device mountpoint fstype")
    # Return all mounted partitions as a nameduple.
    # If all == False return physical partitions only.
    phydevs = []
    with open("/proc/filesystems", "r") as f:
        for line in f:
            if not line.startswith("nodev"):
                phydevs.append(line.strip())

    retlist = []
    with open("/etc/mtab", "r") as f:
        for line in f:
            if not all and line.startswith("none"):
                continue
            fields = line.split()
            device = fields[0]
            mountpoint = fields[1]
            fstype = fields[2]
            if not all and fstype not in phydevs:
                continue
            if device == "none":
                device = ""
            ntuple = disk_ntuple(device, mountpoint, fstype)
            retlist.append(ntuple)
    return retlist


def get_mount_point(pathname):
    pathname = os.path.normcase(os.path.realpath(pathname))
    parent_device = path_device = os.stat(pathname).st_dev
    while parent_device == path_device:
        mount_point = pathname
        pathname = os.path.dirname(pathname)
        if pathname == mount_point:
            break
        parent_device = os.stat(pathname).st_dev
    return mount_point


def convertedUnit(n):
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


def serviceMenuOption() -> None:
    status = os.system("systemctl is-active --quiet harmony")
    if status == 0:
        print(
            "*  [8] "
            + Fore.RED
            + "Stop Harmony Service      "
            + Fore.WHITE
            + "- "
            + Fore.YELLOW
            + Back.RED
            + "WARNING: You will miss blocks while stopped!   "
            + Style.RESET_ALL
        )
        print(
            "*  [9] Restart Harmony Service   - "
            + Back.RED
            + Fore.YELLOW
            + "WARNING: You will miss blocks during a restart!"
            + Style.RESET_ALL
        )
    else:
        print("*  [8] " + Fore.GREEN + "Start Harmony Service" + Style.RESET_ALL)


def makeBackupDir() -> str:
    if not os.path.isdir(f"{validatorToolbox.harmonyDirPath}/harmony_backup"):
        printStarsReset()
        print("Backup directory not found, creating folder")
        os.system(f"mkdir -p {validatorToolbox.harmonyDirPath}/harmony_backup")


def hmyCLIUpgrade():
    printStarsReset()
    question = askYesNo(
        "Are you sure you would like to proceed with updating the Harmony CLI file?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        os.chdir(f"{validatorToolbox.harmonyDirPath}")
        makeBackupDir()
        os.system(f"cp {validatorToolbox.hmyAppPath} {validatorToolbox.harmonyDirPath}/harmony_backup")
        printStars()
        installHmyApp(validatorToolbox.harmonyDirPath)
        printStars()
        print("Harmony cli has been updated to: ")
        os.system(f"{validatorToolbox.hmyAppPath} version")
        printStars()
        input("Update completed, press ENTER to return to the main menu. ")


def upgradeHarmonyApp(testOrMain):
    os.chdir(f"{validatorToolbox.harmonyDirPath}")
    printStarsReset()
    print("Currently installed version: ")
    os.system("./harmony -V")
    makeBackupDir()
    os.system(f"cp {validatorToolbox.harmonyDirPath}/harmony {validatorToolbox.harmonyDirPath}/harmony_backup")
    printStars()
    print("Downloading current harmony binary file from harmony.one: ")
    printStars()
    installHarmonyApp(validatorToolbox.harmonyDirPath, validatorToolbox.blsKeyFile)
    printStars()
    print("Updated version: ")
    os.system("./harmony -V")
    os.system("sudo service harmony restart")
    printStars()
    print(
        "Harmony Service is restarting, waiting 10 seconds for restart."
    )
    time.sleep(10)


def runStats() -> str:
    timeNow = datetime.now()
    ourShard = environ.get("SHARD")
    ourNetwork = environ.get("NETWORK_SWITCH")
    remote_shard_0 = [f'{validatorToolbox.hmyAppPath}', 'blockchain', 'latest-headers', f'--node=https://api.s0.{ourNetwork}.hmny.io']
    result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
    remote_shard = [f'{validatorToolbox.hmyAppPath}', 'blockchain', 'latest-headers', f'--node=https://api.s{ourShard}.{ourNetwork}.hmny.io']
    try:
        result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        remote_data_shard = json.loads(result_remote_shard.stdout)
    except (ValueError, KeyError, TypeError):
        print(f"""
        {stringStars()}
        * Current Date & Time: {timeNow}
        *
        {stringStars()}
        """)
        shardStats(ourShard)
        {stringStars()}
        input(f"* No remote data returned, RPC may be unresponsive. Wait few moments and try again. Press ENTER to return to the main menu.")
        {stringStars()}
        return
    local_shard = [f'{validatorToolbox.hmyAppPath}', 'blockchain', 'latest-headers']
    try:
        result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        local_data_shard = json.loads(result_local_shard.stdout)
    except (ValueError, KeyError, TypeError):
        print(f"""
        {stringStars()}
        * Current Date & Time: {timeNow}
        *
        {stringStars()}
        """)
        shardStats(ourShard)
        {stringStars()}
        input(f"* No local data detected, did you just restart Harmony? Wait a few moments and try again. Press ENTER to return to the main menu.")
        {stringStars()}
        return
    print(f"""
{stringStars()}
* Current Date & Time: {timeNow}
*
{stringStars()}
* Current Status of our server {validatorToolbox.serverHostName} currently on Shard {environ.get('SHARD')}:
*
* Shard 0 Sync Status:
* Local Server  - Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} - Shard {local_data_shard['result']['beacon-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard_0['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}
*
{stringStars()}
    """)
    if int(ourShard) > 0:
        print(f"""
* Shard {ourShard} Sync Status:
*
* Local Server  - Epoch {local_data_shard['result']['shard-chain-header']['epoch']} - Shard {local_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}
* Remote Server - Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} - Shard {remote_data_shard['result']['shard-chain-header']['shardID']} - Block {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}
*
{stringStars()}
    """)
    shardStats(ourShard)
    input("* Validator stats completed, press ENTER to return to the main menu. ")


def getDBSize(ourShard) -> str:
    harmonyDBSize = subprocess.getoutput(f"du -h {validatorToolbox.harmonyDirPath}/harmony_db_{ourShard}")
    harmonyDBSize = harmonyDBSize.rstrip('\t')
    countTrim = len(validatorToolbox.harmonyDirPath) + 13
    return harmonyDBSize[:-countTrim]


def shardStats(ourShard) -> str:
    ourUptime = subprocess.getoutput("uptime")
    ourVersion = subprocess.getoutput(f"{validatorToolbox.harmonyAppPath} -V")
    dbZeroSize = getDBSize('0')
    if ourShard == "0":
        print(f"""
* Uptime :: {ourUptime}\n\n Harmony DB 0 Size  ::  {dbZeroSize}
* {ourVersion}
{stringStars()}
        """)
    else:
        print(f"""
* Uptime :: {ourUptime}
*
* Harmony DB 0 Size  ::  {dbZeroSize}
* Harmony DB {ourShard} Size  ::   {getDBSize(str(ourShard))}
*
* {ourVersion}
*
{stringStars()}
        """)


def menuBinaryUpdates():
    testOrMain = environ.get("NETWORK")
    printStarsReset()
    question = askYesNo(
        Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS WHILE YOU UPGRADE THE HARMONY SERVICE.\n\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        upgradeHarmonyApp(testOrMain)


def menuUbuntuUpdates() -> str:
    printStarsReset()
    question = askYesNo(
        Fore.WHITE
        + "Are you sure you would like to proceed with Linux apt Upgrades?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        osUpgrades()
        print()
        input("OS Updates completed, press ENTER to return to the main menu. ")


def menuRebootServer() -> str:
    printStarsReset()
    question = askYesNo(
        Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS WHILE YOU REBOOT YOUR ENTIRE SERVER.\n\n"
        + "Reconnect after a few moments & Run the Validator Toolbox Menu again with: python3 ~/validator-toolbox/toolbox/start.py\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed with rebooting your server?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        os.system("sudo reboot")
    else:
        print("Invalid option.")


def menuServiceStopStart() -> str:
    status = os.system("systemctl is-active --quiet harmony")
    if status != 0:
        os.system("sudo service harmony start")
        print()
        print("Harmony Service Has Been Started.")
        print()
        input("Press ENTER to return to the main menu.")
    else:
        question = askYesNo(
            "*********\n"
            + Fore.RED
            + "WARNING: YOU WILL MISS BLOCKS IF YOU STOP THE HARMONY SERVICE.\n\n"
            + Fore.WHITE
            + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
        )
        if question:
            os.system("sudo service harmony stop")
            print()
            print(
                "Harmony Service Has Been Stopped. "
                + Fore.RED
                + "YOU ARE MISSING BLOCKS ON THIS NODE."
                + Style.RESET_ALL
            )
            print()
            input("Press ENTER to return to the main menu.")


def menuServiceRestart() -> str:
    question = askYesNo(
        "*********\n"
        + Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS UNTIL RESTART IS COMPLETED & SYNC CATCHES UP!\n\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        os.system("sudo service harmony restart")
        print()
        print("* The Harmony Service Has Been Restarted")
        input("* Press ENTER to return to the main menu.")


def menuActiveBLS() -> str:
    validatorWallet = environ.get('VALIDATOR_WALLET')
    jsonResponse = getWalletJSON(validatorWallet)
    printStarsReset()
    print("* This is a list of your BLS Keys that are active for the next election.")
    for i, x in enumerate(jsonResponse["bls-public-keys"]):
        print(f"BLS Key {i+1} {x}")
    printStars()
    input("Press ENTER to return to the main menu.")


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def menuCheckBalance() -> None:
    validatorWallet = environ.get('VALIDATOR_WALLET')
    if environ.get("NODE_TYPE") == "regular":
        printStarsReset()
        print("* Calling mainnet and testnet for balances...")
        printStars()
        total_balance, total_balance_test = getWalletBalance(validatorWallet)
        print(f"* Your Validator Wallet Balance on Mainnet is: {total_balance} Harmony ONE Coins")
        print(f"* Your Validator Wallet Balance on Testnet is: {total_balance_test} Harmony ONE Test Coins")
        printStars()
        i = 0
        while i < 1:
            question = askYesNo(
                "* Would you like to check another Harmony ONE Address? (YES/NO) "
            )
            if question:
                balanceCheckAny()
            else:
                i = 1
    else:
        i = 0
        while i < 1:
            question = askYesNo(
                "* Would you like to check a Harmony ONE Address? (YES/NO) "
            )
            if question:
                balanceCheckAny()
            else:
                i = 1


def balanceCheckAny():
    printStarsReset()
    checkWallet = input(
        "* Type the address of the Harmony ONE Wallet you would like to check.\n"
        + "* Only one wallets will work, no 0x addresses : "
    )
    print("* Calling mainnet and testnet for balances...")
    printStarsReset()
    total_balance, total_balance_test = getWalletBalance(checkWallet)
    print(f"* The Mainnet Wallet Balance is: {total_balance} Harmony ONE Coins\n* The Testnet Wallet Balance is: {total_balance_test} Harmony ONE Test Coins")
    printStars()
    input("Press ENTER to continue.")


def getCurrentEpoch():
    if environ.get("NETWORK") == "mainnet":
        endpoints_count = len(validatorToolbox.rpc_endpoints)
    if environ.get("NETWORK") == "testnet":
        endpoints_count = len(validatorToolbox.rpc_endpoints_test)

    for i in range(endpoints_count):
        current_epoch = getCurrentEpochByEndpoint(validatorToolbox.rpc_endpoints[i])

        if current_epoch != -1:
            return current_epoch
    current_epoch = 0
    return current_epoch


def getCurrentEpochByEndpoint(endpoint):
    current = 0
    max_tries = validatorToolbox.rpc_endpoints_max_connection_retries
    current_epoch = -1

    while current < max_tries:
        try:
            current_epoch = blockchain.get_current_epoch(endpoint)
            return current_epoch
        except Exception:
            current += 1
            continue

    return current_epoch


def finish_node():
    printStars()
    print("* Thanks for using Easy Node - EZ Mode! Goodbye.")
    printStars()
    raise SystemExit(0)