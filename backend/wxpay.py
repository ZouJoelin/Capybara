import os
import json
import logging

from wechatpayv3 import SignType, WeChatPay, WeChatPayType

from sql import SQL


#############################
# initialize wxpay
#############################

# 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。
if not os.environ.get("MCHID"):
    raise RuntimeError("MCHID not set")
MCHID = os.environ.get("MCHID")

# APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid，也可以在调用接口的时候覆盖。
if not os.environ.get("APPID"):
    raise RuntimeError("APPID not set")
APPID = os.environ.get("APPID")

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
if not os.environ.get("APIV3_KEY"):
    raise RuntimeError("APIV3_KEY not set")
APIV3_KEY = os.environ.get("APIV3_KEY")

# 商户证书序列号
if not os.environ.get("CERT_SERIAL_NO"):
    raise RuntimeError("CERT_SERIAL_NO not set")
CERT_SERIAL_NO = os.environ.get("CERT_SERIAL_NO")

# 商户证书私钥，此文件不要放置在下面设置的CERT_DIR目录里。
if not os.environ.get("PRIVATE_KEY"):
    raise RuntimeError("PRIVATE_KEY not set")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

# 回调地址，也可以在调用接口的时候覆盖。
if not os.environ.get("NOTIFY_URL"):
    raise RuntimeError("NOTIFY_URL not set")
NOTIFY_URL = os.environ.get("NOTIFY_URL")

# 公众号开发者密码(AppSecret)
if not os.environ.get("APP_SECRET"):
    raise RuntimeError("APP_SECRET not set")
APP_SECRET = os.environ.get("APP_SECRET")

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None

# 微信支付平台证书缓存目录，初始调试的时候可以设为None，首次使用确保此目录为空目录。
CERT_DIR = None  # './cert'

# 接入模式：False=直连商户模式，True=服务商模式。
PARTNER_MODE = False

# # 日志记录器，记录web请求和回调细节，便于调试排错。
# logging.basicConfig(filename=os.path.join(os.getcwd(), 'log/wxpay.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
# LOGGER = logging.getLogger("wxpay")

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    appid=APPID,
    apiv3_key=APIV3_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    private_key=PRIVATE_KEY,  
    notify_url=NOTIFY_URL,

    proxy=PROXY,
    cert_dir=CERT_DIR,
    partner_mode=PARTNER_MODE,
    # logger=LOGGER,
)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///capybara.db")

#############################
# wxpay function start here
#############################

# make a trade: native
def pay_native(amount, out_trade_no, description):
    # print("========== in pay_native()==========")
    code, message = wxpay.pay(
        amount={'total': amount},
        out_trade_no=out_trade_no,
        description=description,
        pay_type=WeChatPayType.NATIVE
    )
    message = json.loads(message)
    code_url = message.get('code_url')
    # print("========== end pay_native() ==========")
    return code, code_url


# make a trade: jsapi
def pay_jsapi(amount, out_trade_no, description, open_id):
    # print("========== in pay_jsapi()==========")
    payer = {'openid': open_id}
    code, message = wxpay.pay(
        amount={'total': amount},
        out_trade_no=out_trade_no,
        description=description,
        pay_type=WeChatPayType.JSAPI,
        payer=payer
    )
    message = json.loads(message)
    prepay_id = message.get('prepay_id') 
    # print("========== end pay_jsapi() ==========")
    return code, prepay_id


# query for trade state
def query(out_trade_no):
    # print("========== in query()==========")
    code, message = wxpay.query(out_trade_no=out_trade_no)
    # print('>>>>>code: %s \n>>>>>message: %s' % (code, message))

    # parse message
    message = json.loads(message)
    # for key in message.keys():
    #     print(">>>>>"+ key +":     ", message[key])
    #     print(">>>>>type of " + key +":     ", type(message[key]))
        
    trade_state = message.get("trade_state")
    trade_time = message.get("success_time")
    # print(">>>>>trade_state:     ", trade_state)
    # print(">>>>>trade_time:     ", trade_time)
    # print("========== end query() ==========")
    return code, trade_state, trade_time


# parse wx's callback request
def parse_callback(headers, data):
    result = wxpay.callback(headers, data)
    # print(">>>>>CALLBACK_RESULT:     ", result)

    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        response = result.get('resource')
        # mchid = response.get('mchid')
        # appid = response.get('appid')
        out_trade_no = response.get('out_trade_no')
        # transaction_id = response.get('transaction_id')
        trade_type = response.get('trade_type')
        trade_state = response.get('trade_state')
        success_time = response.get('success_time')
        # trade_state_desc = response.get('trade_state_desc')
        # bank_type = response.get('bank_type')
        # attach = response.get('attach')
        # payer = response.get('payer')
        # amount = response.get('amount').get('total')
        return {'out_trade_no': out_trade_no, 
                'trade_state':trade_state,
                'trade_time': success_time}

    return None


# close the trade
def close(out_trade_no):
    # print("========== close() ==========")
    code, message = wxpay.close(out_trade_no=out_trade_no)
    # print('>>>>>code: %s \n>>>>>message: %s' % (code, message))
    db.execute("UPDATE print_order SET trade_state = (?) WHERE out_trade_no = (?)", 
            "CLOSED", out_trade_no)
    # print("========== end close() ==========")
    return code, message