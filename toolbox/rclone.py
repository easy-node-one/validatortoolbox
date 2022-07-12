import os
from os import environ
from utils.config import validatorToolbox
from utils.installer import cloneShards, loadVarFile
from utils.library import loaderIntro, getShardMenu

if __name__ == "__main__":
    os.system("clear")
    loaderIntro()
    loadVarFile()
    if not environ.get('SHARD'):
        getShardMenu(validatorToolbox.dotenv_file)
    print(
        "* Harmony ONE Validator Shard Downloader"
    )
    loadVarFile()
    cloneShards()