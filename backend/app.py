

import os
import time
from random import sample
from string import ascii_uppercase, digits

from flask import Flask, session, request, jsonify, abort, make_response, render_template
from flask_session import Session
from flask_mobility import Mobility
import requests
import concurrent.futures

from werkzeug.middleware.proxy_fix import ProxyFix

from sql import SQL
from wxpay import *
from utils import * 


###############################################
# initialize Flask.app & session & sqlite
###############################################

NOTIFICATION = "为配合后续共享文库，临时推出用户和印币抵扣模块。目前可通过转发小程序获取印币，限每日两次，每次3枚。"
PRICE_PER_PAGE_ONE = 0.01
PRICE_PER_PAGE_TWO = 0.01
DISCOUNT_PER_COIN = 0.01
UPLOAD_FOLDER = os.getcwd() + "/../files_temp/"
sides_zh = {"one-sided": "单面打印", 
            "two-sided-long-edge": "双面打印，长边翻转", 
            "two-sided-short-edge": "双面打印，短边翻转"}

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

Mobility(app)

# Logger
app.logger.setLevel(logging.INFO)

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
    return make_response(jsonify({'error_message': 'Not Found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error_message': 'Bad Request'}), 400)


###############################################
# Basic Printing
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

    # authorize with wx
    code = request.args.get('code')
    if not code:
        return jsonify({'error_message': 'access_token failed',
                        'reason': 'no code received'}), 401
    token_url = f'https://api.weixin.qq.com/sns/jscode2session?'\
                f'appid={APPID}&secret={APP_SECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(token_url)
    
    response = json.loads(response.text)
    if response.get("errcode"):
        app.logger.error(f">>>>> Access token failed!!! errcode: {response.get('errcode')} errmsg: {response.get('errmsg')}")
        return jsonify({'error_message': 'access_token failed',
                        'reason': response.get("errmsg"),
                        'errcode': response.get("errcode")}), 401
    open_id = response.get("openid")
    session["open_id"] = open_id

    return jsonify({'initialized': 'ok',
                    'open_id': session["open_id"],
                    'notification': NOTIFICATION})


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
    printer_status_dict = {"ok": "ok", 
                          "door_open": "打印机盖未闭合", 
                          "out_of_paper": "打印机纸张不足", 
                          "out_of_toner": "打印机墨粉不足", 
                          "jam": "打印机有纸张堵塞",
                          "offline": "打印机未连接",
                          "unknown_error": "打印机发生未知错误"}
    status = printer_status()
    if status == "ok":
        return jsonify({"backend_status": printer_status_dict[status]}), 200
    else:
        return jsonify({"error_message": printer_status_dict[status]}), 503


@app.route("/local_upload", methods=["POST", "GET"])
def local_upload():
    """upload local file to server.
    
    Request:
        - ["GET"] 
        - ["POST"] with request.form["fileName"], request.form["pages"]

    """
    if request.method == "GET":
        return render_template("localUpload.html")
    else:
        if (not request.form.get("fileName")) or (not request.form.get("pages")):
            return jsonify({'error_message': "fileName&pages required to set session"}), 400
    
        session["filename"] = request.form.get("fileName")
        session["pages"] = int(request.form.get("pages"))

        return jsonify({'fileName': session["filename"],
                        'pages': session["pages"]})


@app.route("/api/auto_count/pages", methods=["POST"])
def count_pages():
    """auto count .pdf pages and save .pdf file 
    
    Request:
        - ["POST"] with request.files
        Response: {"pages": <int>}
        Exception: {"error_message": <str>}
    """
    # print(">>>>>request:     ", request)
    # print(">>>>>file?:     ", request.files)
    # print(">>>>>form?:     ", request.form)
    # print(">>>>>session:     ", request.headers.get("Cookie"))

    if not request.files:
        abort(400)
    file = request.files.get("file")
    if not file:
        abort(400)

    filename = request.form.get("fileName")
    filename = secure_filename(filename)

    # if capture_injection(filename):
    #     return jsonify({'error_message': "Illegal filename!\nNice try. keep going!"}), 403
    
    ## save file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # MUST save file before calling PdfReader(), otherwise PdfReader will corrupt the file.
    if not validate_file(file, filename):
        app.logger.warning(">>>>> Wrong file type!!!")
        return jsonify({'error_message': "请上传正确的pdf文件"}), 400
    
    pages = count_pdf_pages(file)
    session["filename"] = filename
    session["pages"] = int(pages)

    return jsonify({'fileName': session["filename"],
                    'pages': session["pages"]})
    

@app.route("/api/auto_count/fee", methods=["POST"])
def count_fee():
    """auto calculate fee and update session["*"]
    
    Request:
        - ["POST"] with request.form
        Response: {"fee": <int>}
        Exception: {"error_message": <str>}
    """
    # print(">>>>>request:     ", request)
    # print(">>>>>file?:     ", request.files)
    # print(">>>>>form?:     ", request.form)
    # print(">>>>>session:     ", request.headers.get("Cookie"))

    if not session.get("pages"):
        return jsonify({'error_message': "请先上传文件"}), 400

    if not request.form:
        abort(400)
    form = request.form

    ## validate form and update session["*"]
    if form["paper_type"] not in PAPER_TYPE:
        app.logger.warning(">>>>> Wrong paper type!!!")
        return jsonify({'error_message': "请输入正确的纸张类型"}), 400
    if form["color"] not in COLOR:
        app.logger.warning(">>>>> Wrong color choice!!!")
        return jsonify({'error_message': "请输入正确的打印颜色"}), 400
    if form["sides"] not in SIDES:
        app.logger.warning(">>>>> Wrong sides choice!!!")
        return jsonify({'error_message': "请选择正确的单双面选项"}), 400
    if (not form["copies"].isdigit()) or (int(form["copies"]) == 0):
        app.logger.warning(">>>>> Wrong copies input!!!")
        return jsonify({'error_message': "打印份数需为正整数"}), 400
    have_coins = db.execute("SELECT coins FROM users WHERE open_id = (?)", session["open_id"])
    if form["spend_coins"] > have_coins:
        app.logger.warning(">>>>> Not enough coins!!!")
        return jsonify({'error_message': "您的印币不足"}), 400

    session["paper_type"] = form["paper_type"]
    session["color"] = form["color"]
    session["sides"] = form["sides"]
    session["copies"] = int(form["copies"])
    session["spend_coins"] = int(form["spend_coins"])

    # calculate fee
    if session["sides"] == "one-sided":
        session["fee"] = session["pages"] * PRICE_PER_PAGE_ONE * session["copies"]
    else:
        residual = session["pages"] % 2
        session["fee"] = ((session["pages"] - residual) * PRICE_PER_PAGE_TWO + residual * PRICE_PER_PAGE_ONE) * session["copies"]

    # discount
    discount = round(min(session["spend_coins"]*DISCOUNT_PER_COIN, session["fee"]), 2)
    session["spend_coins"] = round(discount/DISCOUNT_PER_COIN)
    session["fee"] = max(session["fee"]-discount, 0.01)

    # print(">>>>>>>>>> session >>>>>>>>>>")
    # for key in session.keys():
    #     print(">>>>>"+ key +":     ", session[key])

    return jsonify({'fee': f"{session['fee']:.2f}",
                    'spend_coins': session["spend_coins"]})


@app.route("/api/print_order_info", methods=["GET"])
@formfilled_required(session, app.logger)
def print_order_info():
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
    
    return jsonify({"filename": str(session["filename"]),
                    "pages": int(session["pages"]),
                    "paper_type": str(session["paper_type"]),
                    "color": str(session["color"]),
                    "sides": str(sides_zh[session["sides"]]),
                    "copies": int(session["copies"]),
                    "spend_coins": int(session["spend_coins"]),
                    "price": str(f"{session['fee']:.2f}")})


@app.route("/api/pay", methods=["GET", "POST"])
@formfilled_required(session, app.logger)
def pay():
    """generate payment link

    """
    # generate out_trade_no
    if request.method == "POST":
        out_trade_no = time.strftime("%Y%m%dT%H%M%S", time.localtime()) + ''.join(sample(ascii_uppercase,3))
        return jsonify({'out_trade_no': out_trade_no})
    

    # generate payment link
    else:
        if not request.args.get("out_trade_no"):
            return jsonify({'error_message': "out_trade_no required"}), 400
        out_trade_no = request.args.get("out_trade_no")
        amount = int(session["fee"] * 100)
        description = f"{session['filename']}（{session['pages']}页-{sides_zh[session['sides']][:2]}-{session['copies']}份）"
        device = "MOBILE" if request.MOBILE else "PC"
        # print(">>>>>amount:     " ,amount)
        # print(">>>>>out_trade_no:     " ,out_trade_no)
        # print(">>>>>description:     " ,description)
        app.logger.info(f'>>>>> print_order:  filename: "{session["filename"]}"; pages: "{session["pages"]}"; copies: "{session["copies"]}"; spend_coins: "{session["spend_coins"]}"; fee: "{session["fee"]}"; out_trade_no: "{out_trade_no}"; device: {device}; ')

        # log into sql
        db.execute("INSERT INTO print_order (user_open_id, filename, pages, paper_type, color, sides, copies, spend_coins, fee, out_trade_no, device, trade_type) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    session["open_id"], session["filename"], session["pages"], session["paper_type"], session["color"], session["sides"], session["copies"], session["spend_coins"], session["fee"],
                    out_trade_no, device, "JSAPI")


        # code, prepay_id = pay_jsapi(amount, out_trade_no, description, session["open_id"])
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(pay_jsapi, amount, out_trade_no, description, session["open_id"])
                code, prepay_id = future.result(timeout=3)  # 设置超时时间
        except concurrent.futures.TimeoutError:
            app.logger.error(">>>>> pay_jsapi() timed out!!!")
            return jsonify({'error_message': "下单超时"}), 500
        except Exception as e:
            app.logger.error(f">>>>> pay_jsapi() failed with exception: {e}")
            return jsonify({'error_message': "下单失败"}), 500

        if code not in range(200, 300):
            app.logger.error(">>>>> pay_jsapi() failed!!!", code)
            return jsonify({'error_message': "下单失败"}), 500
        
        app.logger.info(f">>>>>code:     {code} >>>>>filename:    {session['filename']}")
        timestamp = str(int(time.time()))
        app.logger.info(f">>>>>timestamp:     {timestamp}")
        nonceStr = ''.join(sample(ascii_uppercase + digits, 16))
        app.logger.info(f">>>>>nonceStr:     {nonceStr}")
        package = 'prepay_id=' + prepay_id
        app.logger.info(f">>>>>package:     {package}") 
        signType = 'RSA'
        paySign = wxpay.sign([APPID, timestamp, nonceStr, package])
        app.logger.info(f">>>>>paysign:     {paySign}")

        jsapi_sign = {
            "appId": APPID,
            "timestamp": timestamp,
            "nonceStr": nonceStr,
            "package" : package,
            "signType": signType,
            "paySign": paySign
        }
        app.logger.info(f">>>>>jaspi_sign: {jsapi_sign}")

        return jsonify({"out_trade_no": out_trade_no, 
                        "jsapi_sign": jsapi_sign})


@app.route("/api/polling_query", methods=["GET"])
def polling_query():
    """get print order status.
    
    """
    # print(">>>>>>>>>> polling_query >>>>>>>>>>")
    out_trade_no = request.args.get("out_trade_no")

    # lookup local sql first to avoid unnecessary network requests
    print_order = db.execute("SELECT trade_state FROM print_order WHERE out_trade_no = (?)", out_trade_no)
    app.logger.info(">>>>> print_order:     ", print_order)

    if not print_order:
        app.logger.warning(">>>>> Untracked out_trade_no!!!")
        return jsonify({'error_message': "订单不存在"}), 403

    print_order = print_order[0]
    if print_order["trade_state"] == "SUCCESS":
        # shortcut return
        app.logger.info(f">>>>> trade_state from sql(shortcut): {print_order['trade_state']}")
        return jsonify({'message':  print_order["trade_state"]})  
        
    if print_order["trade_state"] in {"CLOSED", "REFUND"}:
        app.logger.warning(">>>>> print_order already closed!!!")
        return jsonify({'error_message': "该订单已关闭， 请重新下单"}), 403

    # call wxpay.query() according to out_trade_to
    code, trade_state, trade_time = query(out_trade_no)
    app.logger.info(f">>>>> trade_state from wx.query: {trade_state}")
    
    # update sql
    if trade_state != "NOTPAY":
        db.execute("UPDATE print_order SET trade_state = (?), trade_time = (?) WHERE out_trade_no = (?)", 
                trade_state, trade_time, out_trade_no)

    return jsonify({'message': trade_state})  


@app.route("/api/close_print_order", methods=["GET"])
def close_print_order():
    """close out_trade_no.
    
    """
    out_trade_no = request.args.get("out_trade_no")
    code, message = close(out_trade_no)
    # app.logger.info(f">>>>> code: {code}; message: {message}")

    return jsonify({'message': message, 'code': code})


@app.route("/api/notify", methods=['POST'])
def notify():
    """API for wx: process wx's callback request.
    
    Request:
        - ["POST"] from wx
        Response: respone to wx
    """
    result = parse_callback(request.headers, request.data)
    if result:
        # update sql
        db.execute("BEGIN TRANSACTION")
        row = db.execute("SELECT trade_state FROM print_order WHERE out_trade_no = (?)", result["out_trade_no"])
        if row[0]["trade_state"] == "SUCCESS":
            return jsonify({'code': 'SUCCESS', 'message': '成功'}), 200
        db.execute("UPDATE print_order SET trade_state = (?), trade_time = (?) WHERE out_trade_no = (?)", 
                result["trade_state"], result["trade_time"], result["out_trade_no"])
        db.execute("COMMIT")

    # make response to wx's callback
        return jsonify({'code': 'SUCCESS', 'message': '成功'}), 200
    else:
        return jsonify({'code': 'FAIL', 'message': '失败'}), 500
      

@app.route("/api/print_file", methods=["GET"])
@formfilled_required(session, app.logger)
def print_file():
    """execute print command.
    
    """
    out_trade_no = request.args.get("out_trade_no")
    print_order = db.execute("SELECT filename, trade_state, print_state FROM print_order WHERE out_trade_no = (?)", out_trade_no)
    # print(">>>>>out_trade_no:     ", out_trade_no)
    # print(">>>>>print_order:     ", print_order)

    # verify out_trade_no 
    if not print_order:
        app.logger.warning(">>>>> Untracked out_pay_no!!!")
        return jsonify({'error_message': "订单不存在"}), 403
    
    print_order = print_order[0]
    # if print_order["trade_state"] == "NOTPAY":
    #     app.logger.warning(">>>>> Unpaid out_pay_no!!!")
    #     return jsonify({'error_message': "订单未支付，请尝试刷新本页面"}), 403
    
    # elif print_order["trade_state"] == "CLOSED":
    #     app.logger.warning(">>>>> Cloesd out_pay_no!!!")
    #     return jsonify({'error_message': "订单已关闭"}), 403
    
    # else:
    #     if print_order["print_state"] == "SUCCESS":
    #         # capture cheating
    #         app.logger.warning(">>>>> Capture cheating!!!")
    #         return jsonify({'error_message': "订单号所对应文件已打印过"}), 403
        
    if print_order["filename"] != session["filename"]:
        app.logger.warning(">>>>> Filename doesn't match!!!")
        return jsonify({'error_message': "订单号与提交文件不符"}), 403

    # update user's coins
    if session["spend_coins"] > 0:
        db.execute("UPDATE users SET coins = coins - (?) WHERE open_id = (?)", session["spend_coins"], session["open_id"])

    # make print command according to session["*"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], session["filename"])
    # print_state = OSprint(filepath=filepath, session=session, logger=app.logger)
    print_state = "SUCCESS"

    # post-check printer state
    """aborted"""
    # state = printer_state()
    # if state != "ok":
    #     app.logger.error(">>>>> {state}")
    #     return apology(state+"<br>出错啦！请联系管理员", 500)

    # update sql's col: print_stateS
    db.execute("UPDATE print_order SET print_state = (?) WHERE out_trade_no = (?)", 
                print_state, out_trade_no)
    
    if print_state == "FAILED":
        app.logger.error(">>>>> OSprint() failed!!!")
        return jsonify({'error_message': "打印失败"}), 500
    else:
        return jsonify({'message': "正在打印",
                        'filename': session['filename']})

        
###############################################
# User module
###############################################

@app.route("/api/get_user_info", methods=["GET"])
def get_user_info():
    """exchange user info by open_id from database.
    
    """
    open_id = request.args.get("open_id")
    if not open_id == session["open_id"]:
        return jsonify({'error_message': "open_id不匹配"}), 403

    user_info = db.execute("SELECT * FROM users WHERE open_id = (?)", open_id)
    if not user_info:
        return jsonify({'error_message': "用户不存在"}), 403

    user_info = user_info[0]

    return jsonify({"nickname": user_info["nickname"],
                    "student_name": user_info["student_name"],
                    "student_id": user_info["student_id"],
                    "university_region_school": f"{user_info['university']}-{user_info['region']}-{user_info['school']}",
                    "dormitory": user_info["dormitory"],
                    "coins": user_info["coins"]})


@app.route("/api/complete_user_info", methods=["POST"])
def complete_user_info():
    """register user info in database.
    
    """
    if not request.form:
        abort(400)
    form = request.form

    # validate user_info form
    if not form["student_id"].isdigit():
        return jsonify({'error_message': "请输入正确学号"}), 400

    # insert user_info into database
    db.execute("INSERT INTO users (open_id, nickname, student_name, student_id, university, region, school, dormitory) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                form["open_id"], form["nickname"], form["student_name"], form["student_id"], form["university"], form["region"], form["school"], form["dormitory"])

    return jsonify({'message': "register completed"})


def add_user_coin(open_id, coins: int):
    """add coins to user's account.
    
    """
    try:
        db.execute("UPDATE users SET coins = coins + (?) WHERE open_id = (?)", coins, open_id)
    except:
        return False
    return True


@app.route("/api/get_today_share_times", methods=["GET"])
def get_today_share_times():
    """get user's today share times.
    
    """
    open_id = request.args.get("open_id")
    if not session.get("open_id"):
        return jsonify({'error_message': "请先初始化"}), 403
    if not open_id == session["open_id"]:
        return jsonify({'error_message': "open_id不匹配"}), 403

    date = time.strftime("%Y-%m-%d", time.localtime())
    # app.logger.info(f">>>>> date: {date}")
    share_times = db.execute("SELECT share_times FROM share WHERE user_open_id = (?) AND share_date = (?)", open_id, date)
    
    if len(share_times) == 0:
        return jsonify({"share_times": 0})
    else:
        return jsonify({"share_times": share_times[0]["share_times"]})


@app.route("/api/share_incentive", methods=["GET"])
def share_incentive():
    """share incentive.
    
    """
    open_id = request.args.get("open_id")
    incentive = int(request.args.get("incentive"))
    
    if not session.get("open_id"):
        return jsonify({'error_message': "请先初始化"}), 403
    if not open_id == session["open_id"]:
        return jsonify({'error_message': "open_id不匹配"}), 403

    date = time.strftime("%Y-%m-%d", time.localtime())
    share_times = db.execute("SELECT share_times FROM share WHERE user_open_id = (?) AND share_date = (?)", open_id, date)
    
    if len(share_times) == 0:
        db.execute("INSERT INTO share (user_open_id, share_date, share_times) VALUES(?, ?, ?)", open_id, date, 0)
    else:
        db.execute("UPDATE share SET share_times = share_times + 1 WHERE user_open_id = (?) AND share_date = (?)", open_id, date)
    
    incentive_state = add_user_coin(open_id, incentive)
    if incentive_state:
        return jsonify({"message": "印币已赠送"})
    else:
        return jsonify({"error_message": "印币赠送失败"})


if __name__ == "__main__":
    app.run(debug=True)



















