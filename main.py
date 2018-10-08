# python 3.6 32bit
# installed package
# 1. pyqt5
# 3. mysql.connector

import logging
import sys
import os
import time
import datetime as dt
import const.stat as ic
import mysql.connector as conn
import api.kiwoom as kw
import sell.sell as sell
import interface.bot as bot
import urllib.request as req
import urllib.parse as pars
import xml.etree.ElementTree as et
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from logging.handlers import TimedRotatingFileHandler


class Operator(QMainWindow):
    def __init__(self):
        super().__init__()
        # transaction start time
        self.start_time = 90000

        # today
        self.today = time.strftime("%Y%m%d")

        # sub classes init
        self.logger_start()
        self.kiwoom = kw.KiwoomWindow(self)
        self.chatbot_start()
        self.selljob_start()

        # business day check
        if self.bizday_check():
            # api connect
            self.api_connect()
            # db connect
        else:
            self.shut_down()

    def api_connect(self):
        self.kiwoom.comm_connect()

    def chatbot_start(self):
        self.botSmwj = bot.BotSmwj(self)
        self.botSmwj.start()
        self.botSmwj.send_message("smwj-trade is starting up")

    def selljob_start(self):
        self.selljob = sell.SellJob(self)

        self.timer = QTimer(self)
        # every minute
        self.timer.start(60000)
        self.timer.timeout.connect(self.selljob.watch_handler)

    def logger_start(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        formatter = logging.Formatter('[%(levelname)s:%(lineno)s] %(asctime)s > %(message)s')
        self.logger = logging.getLogger()

        fh = TimedRotatingFileHandler("C:\SMWJ_LOG\\etl", when="midnight")
        fh.setFormatter(formatter)
        fh.suffix = "_%Y%m%d.log"

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.INFO)

    def db_connect(self):
        self.cnx = conn.connect(**ic.dbconfig)
        self.cursor = self.cnx.cursor()

    def bizday_check(self):
        url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo'
        query_params = '?' + pars.urlencode(
            {pars.quote_plus('serviceKey'): ic.publicdata['key'], pars.quote_plus('solYear'): self.today[:4],
             pars.quote_plus('solMonth'): self.today[4:6]})

        request = req.Request(url + query_params)
        request.get_method = lambda: 'GET'
        response_body = req.urlopen(request).read()

        root = et.fromstring(response_body)
        holidays = list()
        for locdate in root.iter('locdate'):
            holidays.append(locdate.text)

        bizday = True
        if dt.datetime.today().weekday() >= 5:
            bizday = False
            self.botSmwj.send_message("today is weekend")
        elif self.today in holidays:
            bizday = False
            self.botSmwj.send_message("today is holiday")
        elif self.today[4:8] == '0501':
            bizday = False
            self.botSmwj.send_message("today is mayday")

        return bizday

    def shut_down(self):
        self.botSmwj.send_message("smwj-trade is shutting down")
        os._exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    op = Operator()
    # op.show()
    app.exec_()
