import os
import re

from flask import redirect, render_template, request, session
from functools import wraps

from PyPDF2 import PdfReader, errors

ALLOW_EXTENSIONS = {"pdf"}


#############################
# utils function start here
#############################

# render apology page when something goes wrong
def apology(message, code=400):

    return render_template("apology.html", code=code, message=message), code


# format fee as RMB
def rmb(fee):

    return f"￥{fee:,.2f}"


# capture anti-injection-hack
PATTERN = r'(select|insert|delete|drop|update|truncate)[\s]*'
def capture_injection(s):
     capture = re.search(PATTERN, s, re.IGNORECASE)
     
     return capture is not None


# convert filename to secure-format
def secure_filename(filename):
    # special character repo:
    # , ("_", "__"), ("?", "~q"),
    for old, new in [(" ", "_"), ("\"", "^"), ("\'", "^"), 
                    ("/", "~s"), ("%", "~p"), ("#", "~h"),
                    ("--", "_"), (";", "_")]:
        filename = filename.replace(old, new)

    return filename


# validate file's type
def validate_file(file):
    filename = file.filename

    if "." in filename and \
    filename.rsplit(".", 1)[1].lower() in ALLOW_EXTENSIONS:
        try:
            PdfReader(file)
            return True
        except errors.PdfReadError:
            return False
    return False


# count pdf's pages
def count_pdf_pages(file):
    readpdf = PdfReader(file)
    pages = len(readpdf.pages)
    return pages


def formfilled_required(session):
    """
    Decorate routes to require formfilled. see below:
    https://www.liaoxuefeng.com/wiki/1016959663602400/1017451662295584
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print(">>>>> @decorated >>>>>")
            # print(">>>>>keys:     ", session.keys())

            for key in session.keys():
                # print(">>>>>"+ key +":     ", session[key])
                if session[key] is None:
                    print(">>>>>form unfilled as required!!!")
                    return apology("支付并打印前请完成表格信息")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def OSprint(filepath, session):
    print("========== in OSprint()==========")
    # -o landscape???
    option = "-o media={} -o sides={} -# {}".format(
        session["paper_type"], session["sides"], session["copies"])
    # print(">>>>>option:     ", option)
    os.system(f"echo 'lpr {option}' '{filepath}'")

    response_error = os.system(f"lpr {option} '{filepath}' ")
    # 0: succeeded; !0: failed
    print("========== end OSprint() ==========")
    if response_error == 0:
        return 'SUCCESS'
    else:
        return 'FAILED'
    







