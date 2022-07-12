import os
import time
import dotenv
from os import environ
from dotenv import load_dotenv
from utils.config import validatorToolbox
from utils.library import loaderIntro, setWalletEnv, askYesNo, loadVarFile, firstSetup, printStars, stringStars, recheckVars, passphraseStatus, recoverWallet, configFound
from utils.toolbox import runRegularNode, runFullNode

# load_dotenv("~/.easynode.env")

if __name__ == "__main__":
    # Wipe Screen
    os.system("clear")
    # Load Intro
    loaderIntro()
    # Check for .env file, if it doesn't exist kickoff installation
    if not os.path.exists(validatorToolbox.dotenv_file):
        firstSetup()
    loadVarFile()

    # Verify we've got a wallet ready to go in .env file or try to recover installed wallet if setup
    if not environ.get("VALIDATOR_WALLET"):
        recoverWallet()
        if not environ.get("VALIDATOR_WALLET"):
            print(
                "  * You don't currently have a validator wallet address loaded in your .env file, please edit ~/.easynode.env and add a line with the following info:\n "
                + "  * VALIDATOR_WALLET='validatorONEaddress' "
            )
            input("* Press any key to exit.")
            raise SystemExit(0)
    
    # Config file found, proceed to menu
    configFound()
    
    # Verify we'll run
    if environ.get("SETUP_STATUS") != "2":
        recheckVars()
        passphraseStatus()

    # Run regular node - Validator
    if environ.get("NODE_TYPE") == "regular":
        if not environ.get("VALIDATOR_WALLET"):
            setWalletEnv()
        runRegularNode()
    
    # Run full node - RPC
    if environ.get("NODE_TYPE") == "full":
        runFullNode()

    # Shouldn't get here! Break if you get this far
    print("Uh oh, you broke me! Contact Easy Node")
    raise SystemExit(0)