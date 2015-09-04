# -*- coding: utf-8 -*-

import sys
from flask import Flask, render_template, request, redirect, url_for
import random
import datetime
import logging

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

log = logging.getLogger(__name__)
log.info('Start App')

# Main
class VO(object):
    def __init__(self):
        self._count = 0
        self._price = 0
        self._gain = 0

    def getcount(self):
        return self._count

    def setcount(self, count):
        self._count = count

    def getprice(self):
        return self._price

    def setprice(self, price):
        self._price = price

    def getgain(self):
        return self._gain

    def setgain(self, gain):
        self._gain = gain

    count = property(getcount, setcount)
    price = property(getprice, setprice)
    gain = property(getgain, setgain)

vo = VO()

def pickup_rare():
    random.seed()

    i = random.randint(0, 10000000)

    if i == 7777777:
        _rank = 1
        _gain = 500000000
    elif i < 4:
        _rank = 2
        _gain = 10000000
    elif i < 1000:
        _rank = 3
        _gain = 100000
    elif i < 10000:
        _rank = 4
        _gain = 3000
    elif i < 1000000:
        _rank = 5
        _gain = 300
    else:
        _rank = 0
        _gain = 0

    if _rank == 0:
        _message = u"はずれです"
    else:
        _message = "".join([str(_rank),
                            u" 等当たりです！ ",
                            u"当選金額は ",
                            str(_gain),
                            u"円です"])

    print("".join(["rank:", str(_rank),
                   " gain:", str(_gain)]))
    vo.gain += _gain
    return _message

def turn_rare():
    result = []
    result.append(pickup_rare())
    return result

def turn_10rare():
    result = []
    for v in range(0, 10):
        result.append(pickup_rare())
    return result

# Routing
@app.route('/')
def index():
    title = u"ようこそ"
    message = u"宝くじを買うにはボタンをクリックしてください"
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    t = datetime.datetime.today().strftime("%H:%M:%S")
    message = ""
    if request.method == 'POST':
        result = []
        if 'rare' in request.form:
            message = u"宝くじを 1 枚買いました！"
            vo.price += 300
            vo.count += 1
            result = turn_rare()
        if '10rare' in request.form:
            message = u"宝くじを 10 枚買いました！"
            vo.price += 3000
            vo.count += 1
            result = turn_10rare()
        if 'reset' in request.form:
            message = u"リセットしました"
            vo.price = 0
            vo.count = 0
            vo.gain = 0
            result = ""
        title = message
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
            print(i + 1, u"回目")
            result = turn_10rare()
            for r in result:
                print(r)
    else:
        for i in range(0, num):
            print(i + 1, u"回目")
            result = turn_rare()
            for r in result:
                print(r)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        run_local(sys.argv)
    else:
        app.debug = True
        app.run(host='0.0.0.0', port=3000)
