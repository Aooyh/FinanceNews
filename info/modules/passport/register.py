from flask import jsonify, request, make_response
from info.utils.captcha.captcha import captcha
from flask import current_app
from info import create_app
from info.response_code import *
from info.constants import *

redis_store = create_app()[2]


def register():
    """
    用户注册访问路径
    """
    pass


def image_code():
    """
    验证码切换功能
    用户点击验证码图片时
    通过验证码图片的src请求
    """
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')
    text = captcha.generate_captcha()[1]
    image_data = captcha.generate_captcha()[2]
    if not cur_id:
        return jsonify(errno=RET.NODATA, errmsg=error_map[RET.NODATA])
    try:
        redis_store.set('image_code: %s' % cur_id, text, IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete('image_code: %s' % pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=error_map[RET.DATAERR])
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response


def sms_code():
    """
    短信验证功能
    在点击获取验证码时
    通过main.js的sendSMSmsg方法中的ajax请求
    """


