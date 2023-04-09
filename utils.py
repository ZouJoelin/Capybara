
import os

from flask import redirect, render_template, request, session

ALLOW_EXTENSIONS = {"pdf"}

# render apology page when something goes wrong
def apology(message, code=400):

    return render_template("apology.html", code=code, message=message), code


# format fee as RMB
def rmb(fee):

    return f"￥{fee:,.2f}"


# validate file's type
def validate_file(filename):
    print(">>>>>inside validate_file()")
    return "." in filename and \
    filename.rsplit(".", 1)[1].lower() in ALLOW_EXTENSIONS


# secure input string for anti-injection-hack
def secure_string(s):
     """ToDo"""
     s=s
     
     return s


# convert filename to secure-format
def secure_filename(filename):
    filename = secure_string(filename)

    # special character repo:
    # ("-", "--"), ("_", "__"), ("?", "~q"),
    for old, new in [(" ", "_"), ("\"", "^"), ("\'", "^"), 
                    ("/", "~s"), ("%", "~p"), ("#", "~h")]:
        filename = filename.replace(old, new)

    return filename



def formfilled_required(f):
    """ToDo"""    
    
    return


# return the useful infomation in message
def parse(message):

    return


def OSprint():

    return
    







