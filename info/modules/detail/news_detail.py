from flask import render_template, g, current_app, jsonify, abort
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
        news_rank = News.query.order_by(News.clicks.desc()).limit(8).all()
        news_rank_list = [news.to_dict() for news in news_rank]
        comment_obj_list = news_obj.comments
        comment_likes = ''
        collect_news = ''
        is_collect = False
        if g.user:
            comment_likes = g.user.comment_likes
            collect_news = g.user.collection_news
        if collect_news:
            if news_obj in collect_news:
                is_collect = True
        if news_obj:
            news = news_obj.to_dict()
            author_obj = User.query.filter(User.nick_name == news_obj.source).first()
            if author_obj:
                author = author_obj.to_dict()
            else:
                author = ''
            comment_list = list()
            comment_like_ids = [comment_like.comment_id for comment_like in comment_likes]
            for comment_obj in comment_obj_list:
                comment = comment_obj.to_dict()
                if comment.get('id') in comment_like_ids:
                    comment['is_like'] = True
                else:
                    comment['is_like'] = False
                comment_list.append(comment)
            return render_template('detail.html', news=news, comment_list=comment_list,
                                   news_list=news_rank_list, author=author, user_info=g.user_info,
                                   is_collect=is_collect)
        else:
            abort(404)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
