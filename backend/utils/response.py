# 统一返回格式
from flask import jsonify

SUCCESS_CODE = 0
ERROR_CODE = 1

def success(data=None, msg="success"):
    """
        成功返回
    """
    return jsonify({
        "code": SUCCESS_CODE,
        "msg": msg,
        "data": data
    })

def error(msg="error", code=ERROR_CODE):
    """
        失败返回
    """
    return jsonify({
        "code": code,
        "msg": msg,
        "data": None
    })