from . import api_bp
from flask import jsonify, request

@api_bp.route("/confirmData", methods=('GET','POST'))
def confirmData():
    print(request)
    if request.method == "POST":
        print(request.data)
        return "hello", 200
    return "hello", 200
