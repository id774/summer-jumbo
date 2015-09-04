# -*- coding: utf-8 -*-

import sys
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import datetime

app = Flask(__name__)

# Main
class VO(object):
    def __init__(self):
        self._count = 0
        self._price = 0

    def getcount(self):
        return self._count

    def setcount(self, count):
        self._count = count

    def getprice(self):
        return self._price

    def setprice(self, price):
        self._price = price

    count = property(getcount, setcount)
    price = property(getprice, setprice)

vo = VO()

def pickup_premium():
    """UR の景品を確定して排出する"""
    ur = ["二穂", "雪枝", "華賀利", "真乃", "楓", "依咲里", "天音",
          "陽奈", "いつみ", "紗々", "あから", "小織"]
    return np.random.choice(ur)

def pickup_rare(weight):
    """重みに応じてレアガチャを排出する"""
    rarities = ["R", "SR", "UR"]
    picked_rarity = np.random.choice(rarities, p=weight)

    if picked_rarity == "UR":
        picked_rarity = "".join((picked_rarity, "(", pickup_premium(), ")"))

    return picked_rarity

def turn_rare():
    """レアガチャを回す"""
    result = []
    # 小数点第三位を切り上げて 94.85%, 5.04%, 0.12%
    weight = [0.94849, 0.0504, 0.00111]
    result.append(pickup_rare(weight))
    print(weight, result[0])
    return result

def turn_10rare():
    """10 連レアガチャを回す"""
    result = []
    # 小数点第三位を切り上げて 90.28%, 9.29%, 0.45%
    weight = [0.90278, 0.09281, 0.00441]
    for v in range(0, 9):
        result.append(pickup_rare(weight))
    result.append("SR")
    print(weight, result)
    return result

def turn_toku10():
    """特効 10 連レアガチャを回す"""
    result = []
    # 小数点第三位を切り上げて 88.65%, 11.13%, 0.24%
    weight = [0.88648, 0.11121, 0.00231]
    for v in range(0, 9):
        result.append(pickup_rare(weight))
    result.append("SR")
    print(weight, result)
    return result

def turn_toku():
    """特効レアガチャを回す"""
    result = []
    # 小数点第三位を切り上げて 89.31%, 10.46%, 0.24%
    weight = [0.8931, 0.10459, 0.00231]
    result.append(pickup_rare(weight))
    print(weight, result[0])
    return result

# Routing
@app.route('/')
def index():
    title = "ようこそ"
    message = "ガチャを回すにはボタンをクリックしてください"
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    t = datetime.datetime.today().strftime("%H:%M:%S")
    message = ""
    if request.method == 'POST':
        result = []
        if 'rare' in request.form:
            title = "レアガチャを回しました！"
            vo.price = vo.price + 300
            vo.count = vo.count + 1
            result = turn_rare()
        if '10rare' in request.form:
            title = "10 連レアガチャを回しました！"
            vo.price = vo.price + 3000
            vo.count = vo.count + 1
            result = turn_10rare()
        if 'toku10' in request.form:
            title = "特効 10 連レアガチャを回しました！"
            vo.price = vo.price + 3000
            vo.count = vo.count + 1
            result = turn_toku10()
        if 'toku' in request.form:
            title = "特効レアガチャを回しました！"
            vo.price = vo.price + 300
            vo.count = vo.count + 1
            result = turn_toku()
        if 'reset' in request.form:
            title = "リセットしました"
            vo.price = 0
            vo.count = 0
            result = ""
            message = "リセットしました"
        return render_template('index.html',
                               result=result, title=title,
                               time=t, vo=vo,
                               message=message)
    else:
        return redirect(url_for('index'))


def run_local(args):
    num = int(args[1])
    if (num % 10) == 0:
        count_f = num / 10
        for i in range(0, int(count_f)):
            print(i + 1, "回め")
            if len(args) == 3 and args[2] == "toku":
                turn_toku10()
            else:
                turn_10rare()
    else:
        for i in range(0, num):
            print(i + 1, "回め")
            if len(args) == 3 and args[2] == "toku":
                turn_toku()
            else:
                turn_rare()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        run_local(sys.argv)
    else:
        app.debug = True
        app.run(host='0.0.0.0', port=3000)
