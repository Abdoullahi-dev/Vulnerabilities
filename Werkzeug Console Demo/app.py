from flask import Flask, render_template, request, jsonify, abort
import sys, io, contextlib, traceback, os
from functools import wraps
import hmac
import hashlib
import secrets

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

secrete_key = "TKM{You_are_not_allowed_to_see_this}"

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.debug = True

def get_pin_hash():
    pin = os.environ.get("CONSOLE_PIN", "1234")
    return hmac.new(app.secret_key.encode(), pin.encode(), hashlib.sha256).hexdigest()

def check_pin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pin_hash = request.headers.get("X-Console-Pin-Hash")
        if not pin_hash or not hmac.compare_digest(pin_hash, get_pin_hash()):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html", pin_hash=get_pin_hash())

if __name__ == "__main__":
    if not os.environ.get("WERKZEUG_DEBUG_PIN"):
        os.environ["WERKZEUG_DEBUG_PIN"] = "1234"
    app.run()