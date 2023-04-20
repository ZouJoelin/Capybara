
import os
import time
import json
from random import sample
from string import ascii_uppercase, digits

from flask import Flask, render_template, redirect, request, jsonify, url_for, session
from flask_session import Session
from flask_mobility import Mobility
import requests

from PyPDF2 import PdfReader

from sql import SQL
from wxpay import *
from utils import * 


###############################################
# initialize Flask.app & session & sqlite
###############################################

PRICE_PER_PAGE = 0.01
UPLOAD_FOLDER = os.getcwd() + "/files_temp/"

# Configure application
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')


"""!!!Delete after development!!!"""
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure file upload
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOW_EXTENSIONS"] = ALLOW_EXTENSIONS

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

Mobility(app)

# Custom filter
app.jinja_env.filters["rmb"] = rmb

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///capybara.db")


###############################################
# service logic start here
###############################################

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
# input:    GET request
# output:   render("index.html")
# input:    POST request
# output:   redirect("/")
def index():

    if request.MOBILE and not session.get("open_id"):
        redirect_uri = 'http://campusprinter.nat300.top/wx_auth'
        scope = 'snsapi_base'
        auth_url = f'https://open.weixin.qq.com/connect/oauth2/authorize?'\
                f'appid={APPID}&redirect_uri={redirect_uri}&'\
                f'response_type=code&scope={scope}#wechat_redirect'
        # print(">>>>>auth_url:     ", auth_url)
        return redirect(auth_url)

    if request.method == "POST":
        source = request.form["source"]
        if source == "pay.html":
            # withdraw from pay.html
            print(">>>>>>>>>> withdraw from pay.html >>>>>>>>>>")
            out_trade_no = request.form["out_trade_no"]
            close(out_trade_no)
            return redirect("/")
        else:
            # call reset from index.html
            print(">>>>>>>>>> reset session >>>>>>>>>>")
            session["filename"] = None
            session["pages"] = 0
            session["fee"] = None
            return 'OK'
    else:
        # init session["*"]
        # items = ["filename", "pages", "paper_type", "color", "sides", "copies", "fee"]
        session["filename"] = None
        session["fee"] = None

        return render_template("index.html")


@app.route("/wx_auth")
def wx_auth():
    code = request.args.get('code')
    # print(">>>>>code:     ", code)

    token_url = f'https://api.weixin.qq.com/sns/oauth2/access_token?'\
                f'appid={APPID}&secret={APP_SECRET}&code={code}&grant_type=authorization_code'
    
    response = requests.get(token_url)
    # print(">>>>>response:     ", response)
    # print(">>>>>parsed_response:     ", json.loads(response.text))
    response = json.loads(response.text)

    if response.get("errcode"):
        return apology("access_token failed!!!\n" + response.get("errmsg"))
    
    open_id = response.get("openid")
    # print(">>>>>open_id:     ", open_id)
    session["open_id"] = open_id
    return redirect("/")


@app.route("/auto_count", methods=["POST"])
# input:    POST request: files | form's items
# output:   pages or fee
def auto_count():

    # print(">>>>>request:     ", request)
    # print(">>>>>file?:     ", request.files)
    # print(">>>>>form?:     ", request.form)

    # · save file, count pages
    if request.files:
        ## process file
        print(">>>>>>>>>> received file >>>>>>>>>>")
        file = request.files["file"]
        filename = file.filename
        # print(">>>>>type of filename:     ", type(filename))
        # print(">>>>>original filename:     ", filename)

        if not validate_file(filename):
            return apology("请上传pdf文件")

        filename = secure_filename(filename)
        # print(">>>>>secured filename:     ", filename)

        ## save file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        # print(">>>>>file's save-path:     ", filepath)
        file.save(filepath)
        # print(">>>>>file uploaded successfully!!!")

        ## count pages
        readpdf = PdfReader(file)
        pages = len(readpdf.pages)

        ## update session["*"]
        session["filename"] = filename
        session["pages"] = int(pages)

        return jsonify({'pages': session["pages"]})
    
    # · calculate fee, update session["*"]
    if request.form:
        print(">>>>>>>>>> received form >>>>>>>>>>")
        form = request.form
        # print(">>>>>form:     ", form)

        ## update session["*"]
        for key in form.keys():
            # print(">>>>>" + key + ":     ", form[key])
            if key == "pages":
                continue
            elif key == "copies":
                session[key] = int(form[key])
            else:
                session[key] = form[key]

        ## calculate fee
        session["fee"] = session["pages"] * session["copies"] * PRICE_PER_PAGE
        print(">>>>>>>>>> session >>>>>>>>>>")
        for key in session.keys():
            print(">>>>>"+ key +":     ", session[key])

        return jsonify({'fee': session["fee"]})


@app.route("/pay", methods=["GET", "POST"])
# inout:    POST request
# output:   redirect("/pay?code_url=***&out_trade_no=***")
# input:    GET request
# output:   render("pay.html", form, out_trade_no, code_url)
@formfilled_required(session)
def pay():
    if request.method == "POST":
        # generate trade info
        # print(">>>>>type of FEE:     ", type(session["fee"]))
        # print(">>>>>FEE:     ", session["fee"])

        amount = int(session["fee"] * 100)
        # print(">>>>>amount:     " ,amount)
        out_trade_no = time.strftime("%Y%m%dT%H%M", time.localtime()) + ''.join(sample(ascii_uppercase,3))
        # print(">>>>>out_trade_no:     " ,out_trade_no)
        description = session["filename"]
        # print(">>>>>description:     " ,description)

        if not request.MOBILE:
            print(">>>>> access from pc!!!")
            code, code_url = pay_native(amount, out_trade_no, description)

            if code not in range(200, 300):
                return apology("下单失败", code=code)

            # log into sql
            db.execute("INSERT INTO print_order (id, filename, pages, paper_type, color, sides, copies, fee, out_trade_no, trade_type) VALUES((SELECT MAX(id) + 1 FROM print_order), ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        session["filename"], session["pages"], session["paper_type"], session["color"], session["sides"], session["copies"], session["fee"],
                        out_trade_no, "NATIVE")

            url = url_for('pay', out_trade_no=out_trade_no, code_url=code_url)
            # print(">>>>>url_for:     ", url)
            return redirect(url)

        else:
            print(">>>>>access from mobile!!!")
            code, prepay_id = pay_jsapi(amount, out_trade_no, description, session["open_id"])

            if code not in range(200, 300):
                return apology("下单失败", code=code)
            
            timestamp = str(int(time.time()))
            nonceStr = ''.join(sample(ascii_uppercase + digits, 16))
            package = 'prepay_id=' + prepay_id
            signType = 'RSA'
            paySign = wxpay.sign([APPID, timestamp, nonceStr, package])

            # print(">>>>>timestamp:     ", timestamp)
            # print(">>>>>nonceStr:     ", nonceStr)
            # print(">>>>>package:     ", package) 
            # print(">>>>>paysign:     ", paySign)

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
            url = url_for('pay', out_trade_no=out_trade_no, jsapi_sign=jsapi_sign)
            # print(">>>>>url_for:     ", url)
            return redirect(url)

    else:
        out_trade_no = request.args.get("out_trade_no")
        if request.MOBILE:
            jsapi_sign = request.args.get("jsapi_sign").replace("'", "\"")
            jsapi_sign = json.loads(jsapi_sign)
            # print(">>>>>type of jsapi_sign:     ", type(jsapi_sign))
            # print(">>>>>jsapi_sign:     ", jsapi_sign)
            return render_template("pay.html", out_trade_no=out_trade_no, jsapi_sign=jsapi_sign, form=session)
        else:
            code_url = request.args.get("code_url")
            return render_template("pay.html", out_trade_no=out_trade_no, code_url=code_url, form=session)


@app.route("/polling_query")
# input:    GET request: out_trade_no
# output:   message
def polling_query():

    print(">>>>>>>>>> polling_query >>>>>>>>>>")
    out_trade_no = request.args.get("out_trade_no")
    # print(">>>>>out_trade_no:     ", out_trade_no)

    # lookup local sql first to avoid unnecessary network requests
    print_order = db.execute("SELECT trade_state FROM print_order WHERE out_trade_no = (?)", out_trade_no)
    # print(">>>>>print_order:     ", print_order)

    if not print_order:
        print(">>>>>untracked out_pay_no!!!")
        return apology("oops！订单不存在", 403)

    print_order = print_order[0]
    if print_order["trade_state"] == "SUCCESS":
        # shortcut return
        print(">>>>>shortcut return!!!")
        return jsonify({'message':  print_order["trade_state"]})  
        
    if print_order["trade_state"] in {"CLOSED", "REFUND"}:
        print(">>>>>print_order closed!!!")
        return apology("该订单已关闭， 请重新下单", 403)

    # call wxpay.query() according to out_trade_to
    code, trade_state, trade_time = query(out_trade_no)

    # update sql
    if trade_state != "NOTPAY":
        db.execute("UPDATE print_order SET trade_state = (?), trade_time = (?) WHERE out_trade_no = (?)", 
                trade_state, trade_time, out_trade_no)

    return jsonify({'message': trade_state})  



@app.route("/notify", methods=['POST'])
# input:    POST from wx
# output:   response to wx
def notify():

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
      


@app.route("/print_file", methods=["GET", "POST"])
# input:    GET
#output:    redirect("/print_file")
# input:    POST
# output:   render("print_file.html", filename)
@formfilled_required(session)
def print_file():

    if request.method == "POST":
        print(">>>>>>>>>> print_file >>>>>>>>>>")
        out_trade_no = request.form["out_trade_no"]
        print_order = db.execute("SELECT filename, trade_state, print_state FROM print_order WHERE out_trade_no = (?)", out_trade_no)
        # print(">>>>>out_trade_no:     ", out_trade_no)
        # print(">>>>>print_order:     ", print_order)

        # verify out_trade_no 
        if not print_order:
            print(">>>>>untracked out_pay_no!!!")
            return apology("oops！订单不存在", 403)
    
        print_order = print_order[0]
        if print_order["trade_state"] != "SUCCESS":
            print(">>>>>unpaid out_pay_no!!!")
            return apology("订单未支付", 403)
        else:
            if print_order["print_state"] == "SUCCESS":
                # capture cheating
                print(">>>>>capture cheating!!!")
                return apology("订单所对应文件已打印过", 403)
    
        if print_order["filename"] != session["filename"]:
            print(">>>>>filename doesn't match!!!")
            return apology("订单号与提交文件不符")
    
        # make print command according to session["*"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session["filename"])
        # print(">>>>>filefolder:     ", app.config["UPLOAD_FOLDER"])
        # print(">>>>>filepath:     ", filepath)
        print_state = OSprint(filepath=filepath, session=session)

        # update sql's col: print_stateS
        db.execute("UPDATE print_order SET print_state = (?) WHERE out_trade_no = (?)", 
                    print_state, out_trade_no)
        
        if print_state == "FAILED":
            return apology("打印失败", 500)
        else:
            return redirect("/print_file")
    
    else:
        return render_template("print_file.html", filename = session["filename"])


if __name__ == "__main__":
    app.run(debug=True)
