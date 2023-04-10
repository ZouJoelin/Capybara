

from wechatpayv3 import SignType, WeChatPay, WeChatPayType



#############################
# initialize wxpay
#############################

# 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。
MCHID = '1640853604'

# 商户证书私钥，此文件不要放置在下面设置的CERT_DIR目录里。
with open('./private_security/API_cert/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '610A95E657CCD975E2056DDC64C6709F1D0A3AF1'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = '34zxxLhb6j53V8VqTQLXZq77VN5xLRPt'

# APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid，也可以在调用接口的时候覆盖。
APPID = 'wxb14ed541e1ac2dc3'

# 回调地址，也可以在调用接口的时候覆盖。

NOTIFY_URL = 'http://campusprinter.nat300.top/notify'

# 微信支付平台证书缓存目录，初始调试的时候可以设为None，首次使用确保此目录为空目录。
CERT_DIR = None  # './cert'

# 日志记录器，记录web请求和回调细节，便于调试排错。
# logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
# LOGGER = logging.getLogger("demo")

# 接入模式：False=直连商户模式，True=服务商模式。
PARTNER_MODE = False

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    #    logger=LOGGER,
    partner_mode=PARTNER_MODE,
    proxy=PROXY)




# make a trade: native
def pay_native(amount, out_trade_no, description):

    print("=============in pay_native()========================")
    print(">>>>>AMOUNT:     ", amount)
    print(">>>>>OUT_TRADE_NO     :    ", out_trade_no)
    print(">>>>>DESCRIPTION:     ", description)

    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )
    print("========================end========================")
    return {'code': code, 'message': message}


# close the trade
def close(out_trade_no):


    return


# query for trade state
def query(out_trade_no):


    return


# receive wx's callback
def callback(header, data):


    return






