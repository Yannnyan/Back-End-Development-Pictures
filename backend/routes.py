from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    res = make_response((data, 200,))
    return res

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    res = make_response()
    try:
        ind = [item["id"] for item in data].index(id)
        res.data = json.dumps(data[int(ind)])
        res.mimetype = "application/json"
        res.status = "200"
    except (ValueError, IndexError) as e:
        res.status = "404"
    return res


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    res = make_response()
    res.mimetype = "application/json"
    print(request.json)
    try:
        id = request.json["id"]
        [item["id"] for item in data].index(id)
        res.status = 302
        res.data = json.dumps({'Message':f"picture with id {id} already present"})
    except (ValueError) as e:
        data.append(request.json)
        res.data = json.dumps(request.json)
        res.status = 201
    return res

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    res = make_response()
    try:
        ind = [item["id"] for item in data].index(id)
        data[ind] = request.json
        res.data = data[ind]
        res.status = 200
    except ValueError:
        res.status = 404
    return res

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    res = make_response()
    try:
        ind = [item["id"] for item in data].index(id)
        res.data = data[ind]
        data.remove(data[ind])
        res.status = 204
    except ValueError:
        res.data = json.dumps({"message": "picture not found"})
        res.status = 404
    return res