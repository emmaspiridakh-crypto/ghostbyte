"""
keep_alive.py
-------------
Fake Flask server ώστε το Render (ή UptimeRobot κλπ) να βλέπει το service
"up" σε port 1000 (ή το PORT env var του Render), ενώ το πραγματικό bot
τρέχει σε ξεχωριστό thread.
"""

import threading
from flask import Flask

import config

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is alive!"


@app.route("/health")
def health():
    return {"status": "ok"}


def run():
    app.run(host="0.0.0.0", port=config.FLASK_PORT)


def keep_alive():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
