

import os
import time
from random import sample
from string import ascii_uppercase, digits

from flask import Flask, session, request, jsonify, abort, make_response
from flask_session import Session
import requests

from werkzeug.middleware.proxy_fix import ProxyFix

from sql import SQL
from wxpay import *
from utils import * 


###############################################
# initialize Flask.app & session & sqlite
###############################################

PRICE_PER_PAGE = 0.01
UPLOAD_FOLDER = os.getcwd() + "/../files_temp/"

PAPER_TYPE = {"A4"}
COLOR = {"黑白"}
SIDES = {"one-sided", "two-sided-long-edge", "two-sided-short-edge"}

# Configure application
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')

# tell flask it is behind a proxy
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_host=1, x_for=1, x_proto=0, x_port=0, x_prefix=0
)

# """!!!Delete after development!!!"""
# # Ensure templates are auto-reloaded
# app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure file upload
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOW_EXTENSIONS"] = ALLOW_EXTENSIONS

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///capybara.db")


###############################################
# pre-configuration
###############################################

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 404)


###############################################
# API
###############################################

@app.route("/", methods=["GET"])
def index():
    """initialize session with open_id, filename, pages, fee.

    Request:
        - ["GET"] with request.args["code"]
        Response: {"initialized": "ok"}
    """

    session["filename"] = None
    session["pages"] = 0
    session["fee"] = None

    code = request.args.get('code')
    token_url = f'https://api.weixin.qq.com/sns/jscode2session?'\
                f'appid={APPID}&secret={APP_SECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(token_url)
    response = json.loads(response.text)

    if response.get("errcode"):
        print(">>>>>Error:     access_token failed!!!", response.get("errmsg"))
        return jsonify({'error_message': 'access_token failed!!!',
                        'reason': response.get("errmsg")})
    open_id = response.get("openid")
    session["open_id"] = open_id

    return jsonify({'initialized': 'ok'})


@app.route("/api/status", methods=["GET"])
def status():
    """pre-check printer status.

    Request:
        - ["GET"]
        Response:{
            backend_status: "ok"            # ok
                            "door_open"     # 打印机盖未闭合
                            "out_of_paper"  # 纸张不足
                            "out_of_toner"  # 墨粉不足
                            "jam"           # 纸张堵塞
                            "offline"       # 打印机未连接
                            "unknown_error" # 未知错误                    
        }
    """
    status = printer_status()
    return jsonify({"backend_status": status})


@app.route("/api/auto_count/pages", methods=["POST"])
def count_pages():
    """auto count .pdf pages and save .pdf file 
    
    Request:
        - ["POST"] with request.files
        Response: {"pages": <int>}
        Exception: {"error_message": <str>}
    """
    print(">>>>>request:     ", request)
    print(">>>>>file?:     ", request.files)
    print(">>>>>form?:     ", request.form)
    print(">>>>>session:     ", request.headers.get("Cookie"))

    if not request.files:
        abort(400)
    print(">>>>>>>>>> received file >>>>>>>>>>")
    file = request.files.get("file")
    

    if not file:
        abort(400)
    # filename = file.filename
    filename = request.form.get("fileName")
    filename = secure_filename(filename)

    # if capture_injection(filename):
    #     return jsonify({'error_message': "Illegal filename!\nNice try. keep going!"}), 403
    
    ## save file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    print(f">>>>>file: {filename} uploaded successfully!!!")

    # MUST save file before calling PdfReader(), otherwise PdfReader will corrupt the file.
    if not validate_file(file):
        print(">>>>>Error:     wrong file type!!!")
        return jsonify({'error_message': "请上传正确的pdf文件"}), 400
    
    pages = count_pdf_pages(file)
    session["filename"] = filename
    session["pages"] = int(pages)

    return jsonify({'pages': session["pages"]})
    

@app.route("/api/auto_count/fee", methods=["POST"])
def count_fee():
    """auto calculate fee and update session["*"]
    
    Request:
        - ["POST"] with request.form
        Response: {"fee": <int>}
        Exception: {"error_message": <str>}
    """
    print(">>>>>request:     ", request)
    print(">>>>>file?:     ", request.files)
    print(">>>>>form?:     ", request.form)
    print(">>>>>session:     ", request.headers.get("Cookie"))

    if not request.form:
        abort(400)
    # print(">>>>>>>>>> received form >>>>>>>>>>")
    form = request.form

    ## validate form and update session["*"]
    if form["paper_type"] not in PAPER_TYPE:
        print(">>>>>Error:     wrong paper type!!!")
        return jsonify({'error_message': "请输入正确的纸张类型"}), 400
    if form["color"] not in COLOR:
        print(">>>>>Error:     wrong color choice!!!")
        return jsonify({'error_message': "请输入正确的打印颜色"}), 400
    if form["sides"] not in SIDES:
        print(">>>>>Error:     wrong sides choice!!!")
        return jsonify({'error_message': "请选择正确的单双面选项"}), 400
    if (not form["copies"].isdigit()) or (int(form["copies"]) == 0):
        print(">>>>>Error:     wrong copies input!!!")
        return jsonify({'error_message': "打印份数需为正整数"}), 400
    
    session["paper_type"] = form["paper_type"]
    session["color"] = form["color"]
    session["sides"] = form["sides"]
    session["copies"] = int(form["copies"])

    ## calculate fee
    if not session.get("pages"):
        return jsonify({'error_message': "请先上传文件"}), 400
    session["fee"] = session["pages"] * session["copies"] * PRICE_PER_PAGE
    # print(">>>>>>>>>> session >>>>>>>>>>")
    # for key in session.keys():
    #     print(">>>>>"+ key +":     ", session[key])

    return jsonify({'fee': f"{session['fee']:.2f}"})


@app.route("/api/order", methods=["GET"])
@formfilled_required(session)
def order():
    """generate order info
    
    Request:
        - ["GET"]
        Response: {
            "filename": <str>,
            "pages": <int>,
            "paper_type": <str>,
            "color": <str>,
            "sides": <str>,
            "copies": <int>,
            "fee": <int>
    }
    """
    sides_zh = {"one-sided": "单面打印", "two-sided-long-edge": "双面打印，长边翻转", "two-sided-short-edge": "双面打印，短边翻转"}
    return jsonify({"filename": str(session["filename"]),
                    "pages": int(session["pages"]),
                    "paper_type": str(session["paper_type"]),
                    "color": str(session["color"]),
                    "sides": str(sides_zh[session["sides"]]),
                    "copies": int(session["copies"]),
                    "price": str(f"{session['fee']:.2f}")})


@app.route("/api/pay", methods=["GET"])
@formfilled_required(session)
def pay():
    """generate payment link

    
    """
    # generate trade info
    amount = int(session["fee"] * 100)
    print(">>>>>amount:     " ,amount)
    out_trade_no = time.strftime("%Y%m%dT%H%M", time.localtime()) + ''.join(sample(ascii_uppercase,3))
    print(">>>>>out_trade_no:     " ,out_trade_no)
    description = session["filename"]
    print(">>>>>description:     " ,description)

    print(f'>>>>>print_order:     filename: "{session["filename"]}"  pages: "{session["pages"]}"  copies: "{session["copies"]}"  fee: "{session["fee"]}"  out_trade_no: "{out_trade_no}"')

    # print(">>>>>access from mobile!!!")
    code, prepay_id = pay_jsapi(amount, out_trade_no, description, session["open_id"])

    if code not in range(200, 300):
        print(">>>>>Error:     pay_jsapi() failed!!!", code)
        return jsonify({'error_message': "下单失败"})
    
    timestamp = str(int(time.time()))
    nonceStr = ''.join(sample(ascii_uppercase + digits, 16))
    package = 'prepay_id=' + prepay_id
    signType = 'RSA'
    paySign = wxpay.sign([APPID, timestamp, nonceStr, package])
    print(">>>>>timestamp:     ", timestamp)
    print(">>>>>nonceStr:     ", nonceStr)
    print(">>>>>package:     ", package) 
    print(">>>>>paysign:     ", paySign)

    # log into sql
    db.execute("INSERT INTO print_order (id, filename, pages, paper_type, color, sides, copies, fee, out_trade_no, trade_type) VALUES((SELECT MAX(id) + 1 FROM print_order), ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                session["filename"], session["pages"], session["paper_type"], session["color"], session["sides"], session["copies"], session["fee"],
                out_trade_no, "JSAPI")

    jsapi_sign = {
        "appId": APPID,
        "timestamp": timestamp,
        "nonceStr": nonceStr,
        "package" : package,
        "signType": signType,
        "paySign": paySign
    }
    return jsonify({"out_trade_no": out_trade_no, 
                    "jsapi_sign": jsapi_sign})





















