from flask import Flask, send_file
import random
import glob

app = Flask(__name__)

PANELS_DIR = "panels/"
IMAGES = []


@app.route("/")
def index():
    return (
        "Go to /random for a random second panel, or "
        "/comic/<comic_num> for a specific panel."
    )


@app.route("/random")
def random_comic():
    return send_file(random.choice(IMAGES), mimetype="image/png")


@app.route("/comic/<comic>")
def specific_panel(comic):
    filename = f"{PANELS_DIR}{comic}.png"
    return send_file(filename, mimetype="image/png")


@app.before_first_request
def init():
    global IMAGES
    IMAGES = glob.glob(f"{PANELS_DIR}*.png")
