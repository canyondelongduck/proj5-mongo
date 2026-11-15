"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

# MongoDB: "db" is the service name in docker-compose.yml
client = MongoClient("mongodb://db:27017/", serverSelectionTimeoutMS=3000)
db = client.brevetsdb
collection = db.controls


# Pages

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404



# AJAX request handlers

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', 200, type=int)
    begin_time = request.args.get('begin_time', None, type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, brevet_dist_km, begin_time)
    close_time = acp_times.close_time(km, brevet_dist_km, begin_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_submit", methods=["POST"])
def _submit():
    """
    Receives the filled-in control rows as JSON and stores them in MongoDB.
    Each Submit REPLACES whatever was stored before (so double-submit
    never creates duplicates).
    """
    data = request.get_json(silent=True)
    if not data or not data.get("controls"):
        return flask.jsonify(
            error="No control times to submit. Enter at least one control distance first."), 400

    docs = []
    for i, c in enumerate(data["controls"], 1):
        if not isinstance(c, dict):
            return flask.jsonify(error="Row {} is malformed.".format(i)), 400
        try:
            km = float(c.get("km"))
        except (TypeError, ValueError):
            return flask.jsonify(error="Row {}: distance is not a number.".format(i)), 400
        if not c.get("open") or not c.get("close"):
            return flask.jsonify(
                error="Row {}: open/close times are missing (bad distance?).".format(i)), 400
        docs.append({
            "km": km,
            "miles": c.get("miles", ""),
            "location": c.get("location", ""),
            "open": c["open"],
            "close": c["close"],
            "brevet_dist_km": data.get("brevet_dist_km"),
            "begin_time": data.get("begin_time"),
        })

    try:
        collection.delete_many({})
        collection.insert_many(docs)
    except PyMongoError as e:
        app.logger.error("Mongo error: {}".format(e))
        return flask.jsonify(error="Database error. Please try again."), 500
    return flask.jsonify(status="ok", count=len(docs))


@app.route("/display")
def display():
    """Shows the stored control times on a new page."""
    try:
        items = list(collection.find({}, {"_id": 0}).sort("km", 1))
    except PyMongoError as e:
        app.logger.error("Mongo error: {}".format(e))
        return flask.render_template(
            "display.html", items=[], error="Could not reach the database."), 500
    return flask.render_template("display.html", items=items, error=None)



app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")