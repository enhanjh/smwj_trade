from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class KiwoomWindow(QAxWidget):

    # 0. class init and comm connect
    def __init__(self, qobject):
        super().__init__()

        # parent object
        self.par = qobject

        # global variable for determining to sell or not
        self.price = dict()
        self.item_names = dict()
        self.min_price = dict()
        self.buy_price = dict()
        self.buy_tot = dict()

        # ocx init
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        
        # register event handler
        self.OnEventConnect.connect(self.event_connect)
        self.OnReceiveTrData.connect(self.event_receive_tr)
        # self.OnReceiveChejanData(self.event_receive_chejan)
        # self.OnReceiveRealData(self.event_receive_real)
        # self.OnReceiveMsg(self.event_receive_msg)

    # 1. comm(api) connect
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    # 2. login event
    def event_connect(self, err_code):
        if err_code == 0:
            self.par.logger.info("login success")
        else:
            self.par.logger.info("login failed")

        self.login_event_loop.exit()

    # 3. tr request
    def tr_request(self, param, rqname, trcode, req_type, scr_num):

        for key, value in param.items():
            self.dynamicCall("SetInputValue(QString, QString)", key, value)

        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, req_type, scr_num)

        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    # 4. tr response
    def event_receive_tr(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):

        if rqname == "OPT10085_req":
            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)

            for i in range(cnt):
                item = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i,
                                        "종목코드").strip()
                item_name = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i,
                                        "종목명").strip()
                price = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i,
                                         "현재가").strip().replace("-", "")
                bp = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i,
                                      "매입가").strip()
                buytot = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i,
                                          "매입금액").strip()
                # tranDay = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "일자").strip()
                # amt = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "보유수량").strip()


                if item in self.price:
                    self.price[item].append(int(price))

                    if int(price) < int(self.min_price[item]):
                        self.min_price[item] = int(price)

                    # carries only 10 items
                    if len(self.price[item]) > 10:
                        self.price[item].pop(0)
                else:
                    self.price[item] = [int(price)]
                    self.min_price[item] = int(price)

                self.buy_price[item] = int(bp)
                self.item_names[item] = item_name
                self.buy_tot[item] = buytot

            self.par.selljob.determine(self.price, self.min_price, self.buy_price)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    # 5. buy and sell request

    # 6. buy and sell response


