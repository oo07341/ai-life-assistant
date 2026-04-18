# 统一返回格式
from flask import jsonify

def success(data=None, msg="success"):
    return jsonify({
        "code": 0,
        "msg": msg,
        "data": data
    })

def error(msg="error", code=1):
    return jsonify({
        "code": code,
        "msg": msg,
        "data": None
    })