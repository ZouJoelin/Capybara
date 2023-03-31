
import os
from flask import Flask, render_template, request, jsonify
# from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

#################################################
# initialize wechatpay...
#################################################

from wxpay import *

#################################################

UPLOAD_FOLDER = os.getcwd() + "/../files/"
ALLOW_EXTENSIONS = {".pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOW_EXTENSIONS"] = ALLOW_EXTENSIONS


# ToDo: extract the page number of documents...
################ DOCX (pkg: unzip) ##################
# unzip -p 'sample.docx' docProps/app.xml | grep -oP '(?<=\<Pages\>).*(?=\</Pages\>)'
################ DOC (pkg: wv) ######################
# wvSummary sample.doc | grep -oP '(?<=of Pages = )[ A-Za-z0-9]*'
################ PDF (pkg: poppler-utils) ###########
# pdfinfo sample.pdf | grep -oP '(?<=Pages:          )[ A-Za-z0-9]*'


def allowed_file(fileName):
    return "." in fileName and \
        fileName.rsplit(".", 1)[1].lower() in ALLOW_EXTENSIONS


def OSPrint(fileName):
    # os.path.join(app.config["UPLOAD_FOLDER"])
    path = os.path.join(app.config["UPLOAD_FOLDER"]) + fileName

    os.system(f"echo 'lpr -o sides=two-sided-long-edge' '{path}'")
    os.system(f"lpr -o sides=two-sided-long-edge '{path}'")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/countPages", methods=["POST"])
def countPages():
    form = request.form
    print("HELLO 1")
    file = request.files["files"]
    print("HELLO 2")

    fileName = file.filename

    # file = request.form.get("files")
    # file = request.files["files"]
    if file:
        print("HELLO" + fileName)
        os.system("pdfinfo " + fileName +
                  "| grep -oP '(?<=Pages:          )[ A-Za-z0-9]*' ")
        os.system("echo hello")
        pages = os.popen("pdfinfo " + fileName +
                         "| grep -oP '(?<=Pages:          )[ A-Za-z0-9]*' ")
    else:
        pages = "0"
    return render_template("search.html", pages=pages)


@app.route("/wxpay", methods=["POST", "GET"])
def wepay():
    if request.method == "POST":
        form = request.form
        file = request.files["files"]

        fileName = file.filename
        fileNameSecure = secure_filename(fileName)
        print(fileName)
        print(fileNameSecure)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        print("file uploaded successfully!!!")

        #############################
        total_fee = float(form["total_fee"])
        print(">>>>>TOTAL_FEE:     ", type(total_fee))

        result = pay_native(amount=int(total_fee*100))
        print(">>>>>TYPE OF RESULT:     ", type(result))
        print(">>>>>RESULT:     ", result)

        ''' used for jsonfiy return
        result_response = json.loads(result.response[0])
        print(">>>>>TYPE OF RESPONSE:     ", type(result_response))
        print(">>>>>RESPONSE:     ", result_response)
        '''

        message = json.loads(result["message"])
        print(">>>>>TYPE OF MESSAGE:     ", type(message))
        print(">>>>>MESSAGE:     ", message)

        pay_url = message["code_url"]
        print(">>>>>TYPE OF PAY_URL:     ", type(pay_url))
        print(">>>>>PAY_URL:     ", pay_url)

        return render_template("pay.html", file=file, form=form, pay_url=pay_url)


@app.route("/pay_native", methods=["GET"])
def pay_native_test():
    total_fee = float(request.args.get("total_fee"))

    result = jsonify(pay_native(int(total_fee*100)))
    result_response = result.response
    print(">>>>>JSONIFY:     ", result)
    print(">>>>>JSONIFY_response:     ", result_response)

    return result


@app.route("/print", methods=["POST", "GET"])
def printFile():
    if request.method == "POST":
        form = request.form
        fileName = form.get("fileName")
        OSPrint(fileName)
        return render_template("print.html", fileName=fileName)


@app.route('/notify', methods=['POST'])
def notify():
    result = wxpay.callback(request.headers, request.data)
    print(">>>>>CALLBACK_RESULT:     ", result)

    # if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
    #     resp = result.get('resource')
    #     appid = resp.get('appid')
    #     mchid = resp.get('mchid')
    #     out_trade_no = resp.get('out_trade_no')
    #     transaction_id = resp.get('transaction_id')
    #     trade_type = resp.get('trade_type')
    #     trade_state = resp.get('trade_state')
    #     trade_state_desc = resp.get('trade_state_desc')
    #     bank_type = resp.get('bank_type')
    #     attach = resp.get('attach')
    #     success_time = resp.get('success_time')
    #     payer = resp.get('payer')
    #     amount = resp.get('amount').get('total')
    #     # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
    #     return jsonify({'code': 'SUCCESS', 'message': '成功'})
    # else:
    #     return jsonify({'code': 'FAILED', 'message': '失败'}), 500


if __name__ == "__main__":
    app.run(debug=True)
