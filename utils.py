
import os

from flask import redirect, render_template, request, session
from functools import wraps

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



def formfilled_required(session):
    """
    Decorate routes to require formfilled. see below:
    https://www.liaoxuefeng.com/wiki/1016959663602400/1017451662295584
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(">>>>> @decorated >>>>>")
            print(">>>>>keys:     ", session.keys())

            for key in session.keys():
                print(">>>>>"+ key +":     ", session[key])
                if session[key] is None:
                    print("支付并打印前请完成表格信息")
                    return apology("支付并打印前请完成表格信息")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# return the useful infomation in message
def parse(message):

    return


def OSprint():

    return
    







