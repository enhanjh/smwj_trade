OP_ERR_NONE = 0   # 정상처리
OP_ERR_LOGIN = -100   # 사용자정보교환에 실패하였습니다. 잠시후 다시 시작하여 주십시오.
OP_ERR_CONNECT = -101   # 서버 접속 실패
OP_ERR_VERSION = -102   # 버전처리가 실패하였습니다.
OP_ERR_SISE_OVERFLOW = -200   # 시세조회 과부하
OP_ERR_RQ_STRUCT_FAIL = -201   # REQUEST_INPUT_st Failed
OP_ERR_RQ_STRING_FAIL = -202   # 요청 전문 작성 실패
OP_ERR_ORD_WRONG_INPUT = -300   # 주문 입력값 오류
OP_ERR_ORD_WRONG_ACCNO = -301   # 계좌비밀번호를 입력하십시오.
OP_ERR_OTHER_ACC_USE = -302   # 타인계좌는 사용할 수 없습니다.
OP_ERR_MIS_2BILL_EXC = -303   # 주문가격이 20 억원을 초과합니다.
OP_ERR_MIS_5BILL_EXC = -304   # 주문가격은 50 억원을 초과할 수 없습니다.
OP_ERR_MIS_1PER_EXC = -305   # 주문수량이 총발행주수의 1 % 를 초과합니다.
OP_ERR_MID_3PER_EXC = -306   # 주문수량은 총발행주수의 3 % 를 초과할 수 없습니다.


def error_name(error_code):

    error_desc = {
        OP_ERR_NONE: "[" + str(error_code) + "] :" + "정상처리",
        OP_ERR_LOGIN: "[" + str(error_code) + "] :" + "사용자 정보교환에 실패하였습니다.",
        OP_ERR_CONNECT: "[" + str(error_code) + "] :" + "서버 접속 실패",
        OP_ERR_VERSION: "[" + str(error_code) + "] :" + "버전처리가 실패하였습니다",
        OP_ERR_SISE_OVERFLOW: "[" + str(error_code) + "] :" + "시세조회 과부하",
        OP_ERR_RQ_STRUCT_FAIL: "[" + str(error_code) + "] :" + "REQUEST_INPUT_st Failed",
        OP_ERR_RQ_STRING_FAIL: "[" + str(error_code) + "] :" + "요청 전문 작성 실패",
        OP_ERR_ORD_WRONG_INPUT: "[" + str(error_code) + "] :" + "주문 입력값 오류",
        OP_ERR_ORD_WRONG_ACCNO: "[" + str(error_code) + "] :" + "계좌비밀번호를 입력하십시오.",
        OP_ERR_OTHER_ACC_USE: "[" + str(error_code) + "] :" + "타인계좌는 사용할 수 없습니다.",
        OP_ERR_MIS_2BILL_EXC: "[" + str(error_code) + "] :" + "주문가격이 20억원을 초과합니다.",
        OP_ERR_MIS_5BILL_EXC: "[" + str(error_code) + "] :" + "주문가격은 50억원을 초과할 수 없습니다.",
        OP_ERR_MIS_1PER_EXC: "[" + str(error_code) + "] :" + "주문수량이 총발행주수의 1%를 초과합니다.",
        OP_ERR_MID_3PER_EXC: "[" + str(error_code) + "] :" + "주문수량은 총발행주수의 3%를 초과할 수 없습니다"
    }

    return error_desc.get(error_code, "")
