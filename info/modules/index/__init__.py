from flask import current_app, g, jsonify, request
from info.utils.commons import log_in_ifo
from flask import render_template
from info.response_code import *
from info.models import Category, News
from flask import Blueprint

index_blue = Blueprint('index', __name__, template_folder='../../templates/news')


@index_blue.route('/')
@log_in_ifo
def index():
    try:
        categories = Category.query.all()
        news_rank = News.query.limit(10).all()
        category_list = [category.to_dict() for category in categories]
        news_list = [news.to_dict() for news in news_rank]
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    return render_template('index.html', user_info=g.user_info, category_list=category_list, news_list=news_list)


@index_blue.route('/newslist')
def show_news():
    page_info = request.args
    page = int(page_info.get('page'))
    per_page = int(page_info.get('per_page'))
    cid = int(page_info.get('cid'))
    news_list = list()
    try:
        if cid == 1:
            paginate = News.query.order_by(News.create_time.desc()).paginate(page, per_page, False)
        else:
            paginate = News.query.filter(News.category_id == cid).\
                order_by(News.clicks.desc()).paginate(page, per_page, False)
        total_page = paginate.pages
        cur_page = paginate.page
        news_obj_list = paginate.items
        for news in news_obj_list:
            news_info = news.to_dict()
            news_list.append(news_info)
        return jsonify(errno=RET.OK, totalPage=total_page, curPage=cur_page, newsList=news_list)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@index_blue.route('/favicon.ico')
def send_ico():
    return current_app.send_static_file('news/favicon.ico')
