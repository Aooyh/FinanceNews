from flask import Blueprint, render_template, g, current_app, jsonify, abort
from info.utils.commons import log_in_ifo
from info.response_code import *
from info.models import News, User

detail_blue = Blueprint('news_detail', __name__, url_prefix='/news', template_folder='../../templates/news')


@detail_blue.route('/<int:news_id>')
@log_in_ifo
def news_detail(news_id):
    try:
        news_obj = News.query.filter(News.id == news_id).first()
        news_rank = News.query.order_by(News.clicks.desc()).limit(8).all()
        news_rank_list = [news.to_dict() for news in news_rank]
        comment_obj_list = news_obj.comments
        if news_obj:
            news = news_obj.to_dict()
            author_obj = User.query.filter(User.nick_name == news_obj.source).first()
            if author_obj:
                author = author_obj.to_dict()
            else:
                author = ''
            comment_list = [comment.to_dict() for comment in comment_obj_list]
            return render_template('detail.html', news=news, comment_list=comment_list,
                                   news_list=news_rank_list, author=author, user_info=g.user_info)
        else:
            abort(404)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
