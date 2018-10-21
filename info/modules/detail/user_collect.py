from flask import jsonify, request, g, current_app
from info.utils.commons import log_in_ifo
from info.response_code import *
from info.models import News, db


@log_in_ifo
def user_collect():
    """
    用户收藏功能
    :return:
    """
    info_data = request.json
    news_id = info_data.get('news_id')
    action = info_data.get('action')
    try:
        news = News.query.filter(News.id == news_id).first()
        if action == 'collect':
            g.user.collection_news.append(news)
            db.session.commit()
            return jsonify(errno=RET.OK, errmsg='收藏成功')
        else:
            g.user.collection_news.remove(news)
            db.session.commit()
            return jsonify(errno=RET.OK, errmsg='取消收藏成功')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
