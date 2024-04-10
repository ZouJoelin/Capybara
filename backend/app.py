

import os

from flask import Flask, session, request, jsonify, abort, make_response
from flask_session import Session

from werkzeug.middleware.proxy_fix import ProxyFix

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
    session["filename"] = None
    session["pages"] = 0
    session["fee"] = None
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

    if not request.files:
        abort(400)
    print(">>>>>>>>>> received file >>>>>>>>>>")
    file = request.files.get("file")
    if not file:
        abort(400)
    filename = file.filename
    filename = secure_filename(filename)

    # if capture_injection(filename):
    #     return jsonify({'error_message': "Illegal filename!\nNice try. keep going!"}), 403
    
    ## save file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    print(">>>>>file uploaded successfully!!!")

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
    # print(">>>>>request:     ", request)
    # print(">>>>>file?:     ", request.files)
    # print(">>>>>form?:     ", request.form)

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
    session["fee"] = session["pages"] * session["copies"] * PRICE_PER_PAGE
    # print(">>>>>>>>>> session >>>>>>>>>>")
    # for key in session.keys():
    #     print(">>>>>"+ key +":     ", session[key])

    return jsonify({'fee': session["fee"]})

























