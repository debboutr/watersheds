import os

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"csv", "gpkg", "tab", "zip"}

app = Flask(__name__)
app.config.from_envvar("APP_SETTINGS")


@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    print("contents of uploaded:", os.listdir("/uploaded"))
    print("IP:", str(request.remote_addr))
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash(f"No selected file. IP: {request.remote_addr}")
            return redirect(request.url)
        if file:
            print(app.config)
            if not allowed_file(file.filename):
                flash("wrong file type.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Success!")
            return render_template("index.html")
    return render_template("index.html")
