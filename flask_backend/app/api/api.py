from . import api_bp
from flask import request
from .utils import *
import json
from flask import jsonify

@api_bp.route("/confirmData", methods=('GET','POST'))
def confirmData():
    print(request)
    if request.method == "POST":
        data = json.loads(request.data)
        result = knowledge_graph(data["text"])
        print(result)
        return jsonify(result), 200
    # return "hello", 200
