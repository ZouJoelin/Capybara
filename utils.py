
import os

from flask import redirect, render_template, request, session



# render apology page when something goes wrong
def apology(message, code=400):


    return render_template("apology.html", top=code, bottom=message), code


# format fee as RMB
def rmb(fee):

    return f"￥{fee:,.2f}"


# validate file's type
def validate_file(filename):

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
    







