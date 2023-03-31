import json
import logging
from random import sample
from string import ascii_letters, digits

import os
from flask import Flask, jsonify, request

from wechatpayv3 import SignType, WeChatPay, WeChatPayType


#################################################
# initialize wechatpay...
#################################################

# 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。
MCHID = '1640853604'

# 商户证书私钥，此文件不要放置在下面设置的CERT_DIR目录里。
with open('./../keys/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '610A95E657CCD975E2056DDC64C6709F1D0A3AF1'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = '34zxxLhb6j53V8VqTQLXZq77VN5xLRPt'

# APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid，也可以在调用接口的时候覆盖。
APPID = 'wxb14ed541e1ac2dc3'

# 回调地址，也可以在调用接口的时候覆盖。

NOTIFY_URL = 'http://campusprinter.nat300.top/notify'
# 'http://127.0.0.1:8000/notify'

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


#######################################

app = Flask(__name__)


@app.route('/')
def pay_native(amount=1):
    # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    description = 'demo-description'
#    amount = 1
    print("=============in pay_native()========================")
    print("VERIFY DESCRIP:    ", description)
    print("VERIFY OUT_TRADE:    ", out_trade_no)
    print("VERIFY AMOUNT:    ", amount)
    print("VERIFY PAY TYPE:    ", WeChatPayType.NATIVE)

    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )

    return {'code': code, 'message': message}


# @app.route('/notify', methods=['POST'])
# def notify():
#     result = wxpay.callback(request.headers, request.data)
#     if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
#         resp = result.get('resource')
#         appid = resp.get('appid')
#         mchid = resp.get('mchid')
#         out_trade_no = resp.get('out_trade_no')
#         transaction_id = resp.get('transaction_id')
#         trade_type = resp.get('trade_type')
#         trade_state = resp.get('trade_state')
#         trade_state_desc = resp.get('trade_state_desc')
#         bank_type = resp.get('bank_type')
#         attach = resp.get('attach')
#         success_time = resp.get('success_time')
#         payer = resp.get('payer')
#         amount = resp.get('amount').get('total')
#         # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
#         return jsonify({'code': 'SUCCESS', 'message': '成功'})
#     else:
#         return jsonify({'code': 'FAILED', 'message': '失败'}), 500


if __name__ == "__main__":
    app.run(debug=True)
