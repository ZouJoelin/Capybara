
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd() + "/../files/"
ALLOW_EXTENSIONS = {".pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOW_EXTENSIONS"] = ALLOW_EXTENSIONS


## ToDo: extract the page number of documents...
################ DOCX (pkg: unzip) ##################
# unzip -p 'sample.docx' docProps/app.xml | grep -oP '(?<=\<Pages\>).*(?=\</Pages\>)'
################ DOC (pkg: wv) ######################
# wvSummary sample.doc | grep -oP '(?<=of Pages = )[ A-Za-z0-9]*'
################ PDF (pkg: poppler-utils) ###########
# pdfinfo sample.pdf | grep -oP '(?<=Pages:          )[ A-Za-z0-9]*'


def allowed_file(fileName):
    return "." in fileName and \
            fileName.rsplit(".",1)[1].lower() in ALLOW_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wxpay", methods=["POST","GET"])
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

        return render_template("pay.html", file = file, form = form)


if __name__ == "__main__":
    app.run(debug=True)

