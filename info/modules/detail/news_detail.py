from flask import render_template, g, current_app, jsonify, abort, request
from info.utils.commons import log_in_ifo
from info.response_code import *
from info.models import News, User


@log_in_ifo
def news_detail(news_id):
    """
    显示新闻详细信息页面
    :param news_id:
    :return:
    """
    try:
        news_obj = News.query.filter(News.id == news_id).first()
        if not news_obj:
            abort(404)
        news_obj.clicks += 1
        news = news_obj.to_dict()
        news_rank = News.query.order_by(News.clicks.desc()).limit(8).all()
        news_rank_list = [news.to_dict() for news in news_rank]
        comment_obj_list = news_obj.comments
        comment_list = [comment.to_dict() for comment in comment_obj_list]
        is_collect = False
        author_obj = User.query.filter(news_obj.source == User.nick_name).first()
        author = author_obj
        if author:
            author = author.to_dict()
        if not g.user:
            return render_template('detail.html', news=news, comment_list=comment_list,
                                   news_list=news_rank_list, author=author, user_info=g.user_info,
                                   is_collect=is_collect)
        user_like = g.user.comment_likes
        user_like_id = [like_con.comment_id for like_con in user_like]
        if author:
            if g.user in author_obj.followers:
                author['is_followed'] = True
        for comment in comment_list:
            if comment['id'] in user_like_id:
                comment['is_like'] = True
        if news_obj in g.user.comment_likes:
            is_collect = True
        return render_template('detail.html', news=news, comment_list=comment_list,
                               news_list=news_rank_list, author=author, user_info=g.user_info,
                               is_collect=is_collect)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def follow():
    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg=error_map[RET.SESSIONERR])
    follow_info = request.json
    author_id = follow_info.get('user_id')
    action = follow_info.get('action')
    author = User.query.get(author_id)
    if action == 'follow':
        g.user.followed.append(author)
        return jsonify(errno=RET.OK, errmsg='关注成功')
    else:
        g.user.followed.remove(author)
        return jsonify(errno=RET.OK, errmsg='取消关注成功')
