import datetime
import const.stat as ic
from PyQt5.QtCore import *


class SellJob:
    def __init__(self, qobject):
        # parent object
        self.par = qobject
        self.today = datetime.date.today()

    # timer handler
    def watch_handler(self):
        current_time = QTime.currentTime()
        curtime = int(current_time.toString("HHmmss"))
        self.par.logger.info("watch handler : " + current_time.toString("HH:mm:ss"))

        # retrieve account items
        if int(self.par.start_time) <= curtime < int(self.par.start_time+64000):
            self.acct_items()
        # program ends
        elif int(curtime) >= int(self.par.start_time)+70000:
            self.par.shut_down()

    # update unsold items


    # retrieve account items
    def acct_items(self):
        self.par.logger.info("retrieve account items")

        param = dict()
        param["계좌번호"] = ic.telegram["accnt_no"]

        self.par.kiwoom.tr_request(param, "OPT10085_req", "OPT10085", 0, "5454")

    # determine to sell or not, notify when certain condition is met
    def determine(self, price, min_price, buy_price):
        self.par.logger.info("determine")

        for key, value in price.items():
            # filter today's sold item
            if int(buy_price[key]) <= 0:
                continue

            rate = round((int(value[-1]) - int(buy_price[key])) / int(buy_price[key]), 2)
            self.par.logger.info(str(key) + " | current : " + str(value[-1]) + ", rate : " + str(rate))

            # rate should be greater than 1%
            if rate > 0.01:
                # sell when it goes down less than minimum of 10 minutes
                if int(value[-1]) <= int(min_price[key]):
                    self.sell_order(key, value[-1])

    # sell order(api call and db insert)
    def sell_order(self, item, price):
        print(item + " : " + price)

    # sell order callback(db update)