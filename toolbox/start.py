import os
import time
import dotenv
from os import environ
from dotenv import load_dotenv
from utils.config import validatorToolbox
from utils.library import loaderIntro, setWalletEnv, askYesNo, loadVarFile, firstSetup, printStars, recheckVars, passphraseStatus, recoverWallet
from utils.toolbox import runRegularNode, runFullNode

# load_dotenv("~/.easynode.env")

if __name__ == "__main__":
    os.system("clear")
    loaderIntro()
    if not os.path.exists(validatorToolbox.dotenv_file):
        firstSetup()
    loadVarFile()
    if not environ.get("VALIDATOR_WALLET"):
        recoverWallet()
        if not environ.get("VALIDATOR_WALLET"):
            print(
                "* You don't currently have a validator wallet address loaded in your .env file, please edit ~/.easynode.env and add a line with the following info:\n "
                + "* VALIDATOR_WALLET='validatorONEaddress' "
            )
            input("* Press any key to exit.")
            raise SystemExit(0)
    print("* Configuration file detected, loading the validatortoolbox menu application.")
    printStars()
    if environ.get("SETUP_STATUS") != "2":
        recheckVars()
        passphraseStatus()
    if environ.get("NODE_TYPE") == "regular":
        if not environ.get("VALIDATOR_WALLET"):
            setWalletEnv()
        runRegularNode()
    if environ.get("NODE_TYPE") == "full":
        runFullNode()
    print("Uh oh, you broke me! Contact Easy Node")
    raise SystemExit(0)