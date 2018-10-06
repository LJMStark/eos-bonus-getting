import json
import os
import pickle
from time import sleep

import execjs
import requests

from log import loggingSetting
from ut import getAccounts, pushaction, unlock

s = requests.Session()
logger = loggingSetting("draw")


current_dir = os.path.dirname(os.path.abspath(__file__))
betdiceFile = os.path.join(current_dir, "betdice.js")
with open(betdiceFile, "r") as f:
    jscode = f.read()
ctx = execjs.compile(jscode)


def main(password):
    x = getAccounts()
    for i in x:
        t = getdraw(i)
        if b"wrong identity" in t:
            sleep(1)
            print("*" * 60)
            getdraw(i)
        print(t)


def getdraw(account):
    b, c = randomN(account)
    return pushaction("betdicelucky", "draw", [account, b, c], account)


def randomN(account):
    blocknum = getinfo()
    data = {"name": account, "blocknum": blocknum}
    z = requests.get("http://localhost:5000/betdice", params=data)
    d = z.json()
    b, c = d["b"], d["c"]
    return b, c


def getinfo():
    url = "https://api.eosbeijing.one/v1/{}"
    z1 = s.post(url.format("chain/get_info"))
    return z1.json()["last_irreversible_block_num"]


if __name__ == "__main__":
    password = "1"
    main(password)
