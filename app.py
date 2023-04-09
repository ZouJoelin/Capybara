
import os

from flask import Flask, render_template, redirect, request, jsonify
from flask_session import Session

from sql import SQL
import wxpay
from utils import * 


###############################################
# initialize Flask.app & session & sqlite
###############################################


UPLOAD_FOLDER = os.getcwd() + "./files_temp/"

# Configure application
app = Flask(__name__)


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

# init session["*"]
items = ["filename", "pages", "paper_type", "color", "side", "copies", "fee"]
session = dict.fromkeys(items)

# Custom filter
app.jinja_env.filters["rmb"] = rmb


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///capybara.db")



@app.route("/")
# input:    GET request
# output:   render("index.html")
def index():

    return render_template("index.html")


@app.route("/auto_count", methods=["POST"])
# input:    POST request: files | form's items
# output:   pages, fee
def auto_count():

    file = request.files
    information = request.form
    print(">>>>>request:     ", request)
    print(">>>>>file?:     ", file)
    print(">>>>>info?:     ", information)

    if request.files:
        print(">>>>>received file...")
        # file = request.files["file"]
        # filename = file.filename
        # print(">>>>>original filename:     ", filename)
        return jsonify({'pages': 12})


    if request.form:
        print(">>>>>received infomation...")
        # information = request.form
        # print(">>>>>infomation:     ", information)
        return jsonify({'fee': 34})


    #     if not validate_file(filename):
    #         return apology("请上传pdf文件")

    #     filename = secure_filename(filename)
    #     print(">>>>>secure filename:     ", filename)

    #     filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    #     print(">>>>>file's save-path:     ", filepath)
    #     file.save(filepath)
    #     print(">>>>>file uploaded successfully!!!")
    #     print(">>>>>return: ",jsonify({"pages": 12}))
    #     return jsonify({'pages': 12})
    
    # else:
    #     print(">>>>>received information...")
    #     information = request.form
    #     print(">>>>>type of copies:     ", type(information["copies"]))
    #     print(">>>>>form's copies:     ", information["copies"])
    #     print(">>>>>return:     ",jsonify({"fee": 34}))

    #     return jsonify({'fee': 34})




    # session["pages"] = count_pages(filename)

    # session["fee"] = calc_fee(pages=session["pages"], copies=session["copies"])


    # update session["*"]
    ## 1. save file, count pages
    ## 2. calculate fee

    # return apology("auto_count: ToDo...")
    # return



@app.route("/pay")
# input:    GET request
# output:   render("pay.html", form, out_trade_no, pay_url)
def pay():
    if request.methods == "POST":
        """ToDO"""
        # withdraw webpage

        return redirect("/")
    
    else:
        """ToDo"""
        # generate trade info

        # call wxpay according to session["fee"]

        # parse message

        return apology("pay: ToDo...")
        return render_template("pay.html")
    

@app.route("/query")
# input:    GET request: out_trade_no
# output:   message
def query():
    """ToDo"""
    # lookup local sql first to avoid unnecessary network requests

    # call utils.query() according to out_trade_to

    # log into sql

    return apology("query: ToDo...")

    return 


@app.route("/notify")
# input:    POST from wx
# output:   response to wx
def notify():
    """ToDo""" 
    # parse the request

    # update sql

    # make response to wx's callback

    return        


@app.route("/print_file")
# input:    GET
# output:   render("print_file.html", filename)
def print_file():
    """ToDO"""
    # make print command according to session["*"]

    # update sql's col: print_stateS

    return apology("print_file: ToDo...")

    return render_template("print_file.html")

if __name__ == "__main__":
    app.run(debug=True)
