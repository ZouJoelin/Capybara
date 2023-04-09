
import os

from flask import redirect, render_template, request, session

ALLOW_EXTENSIONS = {".pdf"}

# render apology page when something goes wrong
def apology(message, code=400):


    return render_template("apology.html", code=code, message=message), code


# format fee as RMB
def rmb(fee):

    return f"￥{fee:,.2f}"


# validate file's type
def validate_file(filename):
    return "." in filename and \
    filename.rsplit(".", 1)[1].lower() in ALLOW_EXTENSIONS


# secure input string for anti-injection-hack
def secure_string(s):
     
     return

# convert filename to secure-format
def secure_filename(filename):

    return


def count_pages(filename):

    return


def calc_fee():

    return


def formfilled_required(f):
    """ToDo"""    
    
    return


# return the useful infomation in message
def parse(message):

    return


def OSprint():

    return
    







