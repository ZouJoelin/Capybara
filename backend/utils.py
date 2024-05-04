import os
import re

from flask import jsonify
from functools import wraps

from PyPDF2 import PdfReader, errors
import cups


ALLOW_EXTENSIONS = {"pdf"}


# detect printer status
def printer_status():
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        printer_state = printers[printer]["printer-state"]
        printer_state_reason = printers[printer]["printer-state-reasons"][0]
        # printer_state_message = printers[printer]["printer-state-message"]
        break

    # print(">>>>>printer state:     ", printer_state)
    # print(">>>>>state_reason:     ", printer_state_reason)
    # print(">>>>>state message:     ", printer_state_message)

    reason_status = {
    "none": "ok",
    "open": "door_open",
    "media-empty": "out_of_paper",
    "toner-empty": "out_of_toner",
    "jam": "jam",
    "offline": "offline",
    "connecting": "offline",
    "unknown_error": "other"
    }

    for reason in reason_status:
        if reason in printer_state_reason:
            return reason_status[reason]
    

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
def validate_file(file, filename):
    # filename = file.filename
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


def formfilled_required(session, logger):
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
                    logger.warning(">>>>>Error:     form unfilled as required!!!")
                    return jsonify({'error_message': "支付并打印前请完成表格信息"}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator


def OSprint(filepath, session, logger):
    # -o landscape???
    option = "-o fit-to-page -o media={} -o sides={} -# {}".format(
        session["paper_type"], session["sides"], session["copies"])
    # print(">>>>>option:     ", option)
    
    logger.info(f"RUN:  lpr {option}' '{filepath}' (pages: {session['pages']})")

    response_error = os.system(f"lpr {option} '{filepath}' ")
    # 0: succeeded; !0: failed

    if response_error == 0:
        return 'SUCCESS'
    else:
        return 'FAILED'


