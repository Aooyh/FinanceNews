from flask import jsonify, request, make_response
from info.utils.captcha.captcha import captcha
from info.libs.yuntongxun.sms import CCP
from flask import current_app
from manager import redis_store
from info.response_code import *
from info.constants import *
import random

def register():
    """
    用户注册访问路径
    """
    pass


def get_image_code():
    """
    验证码切换功能
    用户点击验证码图片时
    通过验证码图片的src请求
    """
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')
    name, text, image_data = captcha.generate_captcha()
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


def get_sms_code():
    """
    短信验证功能
    在点击获取验证码时
    通过main.js的sendSMSmsg方法中的ajax请求
    """
    msg_dict = request.json
    mobile = msg_dict.get('mobile')
    image_code = msg_dict.get('image_code')
    image_code_id = msg_dict.get('image_code_id')
    current_app.logger.info(image_code_id)
    try:
        session_img_code = redis_store.get('image_code: %s' % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    if session_img_code:
        if image_code.lower() == session_img_code.lower():
            redis_store.delete(image_code_id)
            ccp = CCP()
            msg_info = '%06d' % random.randint(0, 999999)
            try:
                result = ccp.send_template_sms(mobile, [msg_info, SMS_CODE_REDIS_EXPIRES / 60], 1)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.THIRDERR, erromsg=error_map[RET.THIRDERR])
            if result == -1:
                return jsonify(errno=RET.DATAERR, errmsg='短信发送失败')
            else:
                try:
                    redis_store.set('sms_code', msg_info, SMS_CODE_REDIS_EXPIRES)
                    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])
                except Exception as e:
                    current_app.logger.error(e)
                    return jsonify(errno=RET.DATAERR, errmsg=error_map[RET.DATAERR])
        else:
            return jsonify(errno=RET.DATAERR, errmsg='验证码输入错误')
    else:
        return jsonify(errno=RET.DATAEXIST, errmsg='验证码已失效')
