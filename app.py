
import os

from flask import Flask, render_template, redirect, request 

from sql import SQL
import wxpay
from utils import * 
###############################################
# initialize Flask.app & session & sqlite
###############################################


UPLOAD_FOLDER = os.getcwd() + "./files_temp/"
ALLOW_EXTENSIONS = {".pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOW_EXTENSIONS"] = ALLOW_EXTENSIONS

# Custom filter
app.jinja_env.filters["rmb"] = rmb

items = ["filename", "pages", "paper_type", "color", "side", "copies", "fee"]



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///capybara.db")



@app.route("/")
# input:    GET request
# output:   render("index.html")
def index():
    fee = 1234.5678
    return render_template("index.html", fee=fee)


@app.route("/auto_count")
# input:    POST request: files | form's items
# output:   pages, fee
def auto_count():
    """ToDo"""
    # update session["*"]
    ## 1. save file, count pages
    ## 2. calculate fee

    return apology("auto_count: ToDo...")
    return


@app.route("/pay")
# input:    GET request
# output:   render("pay.html", form, out_trade_no, pay_url)
def pay():
    if request.method == "POST":
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

