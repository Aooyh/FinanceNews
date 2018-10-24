from flask import render_template, current_app, jsonify
from flask import request
from info.response_code import *
from info.models import News, Category, db


def news_review():
    """
    新闻审核列表
    :return:
    """
    no_check_news = News.query.filter(News.status != 0)
    condition = request.args.get('search')
    page = int(request.args.get('p', '1'))
    try:
        if condition:
            paginate = no_check_news.filter(News.title.contains(condition)).paginate(page, 8, False)
        else:
            paginate = no_check_news.paginate(page, 8, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    news_obj = paginate.items
    news_list = [news.to_review_dict() for news in news_obj]
    current_page = paginate.page
    total_page = paginate.pages
    data = {
        'news_list': news_list,
        'current_page': current_page,
        'total_page': total_page
    }
    return render_template('news_review.html', data=data)


def review_detail():
    """
    审核的详细信息
    :return:
    """
    try:
        if request.method == 'GET':
            news_id = request.args.get('news_id')
            news_obj = News.query.filter(News.id == news_id).first()
            category = Category.query.filter(Category.id == news_obj.category_id).first().to_dict()
            news = news_obj.to_dict()
            return render_template('news_review_detail.html', news=news, category=category)
        else:
            news_id = request.json.get('news_id')
            news_obj = News.query.filter(News.id == news_id).first()
            if request.json.get('action') == 'accept':
                news_obj.status = 0
                return jsonify(errno=RET.OK, errmsg='审核通过')
            else:
                news_obj.status = -1
                news_obj.reason = request.form.get('reason')
                return jsonify(errno=RET.OK, errmsg='审核未通过')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


def news_edit():
    """
    新闻编辑列表
    :return:
    """
    no_edit_news = News.query
    condition = request.args.get('search')
    page = int(request.args.get('p', '1'))
    try:
        if condition:
            paginate = no_edit_news.filter(News.title.contains(condition)).paginate(page, 8, False)
        else:
            paginate = no_edit_news.paginate(page, 8, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    news_obj = paginate.items
    news_list = [news.to_review_dict() for news in news_obj]
    current_page = paginate.page
    total_page = paginate.pages
    data = {
        'news_list': news_list,
        'current_page': current_page,
        'total_page': total_page
    }
    return render_template('news_edit.html', data=data)


def edit_detail():
    """
    新闻编辑的详细页面
    :return:
    """
    try:
        if request.method == 'GET':
            news_id = request.args.get('news_id')
            news_obj = News.query.filter(News.id == news_id).first()
            categories_obj = Category.query.filter(Category.id > 1).all()
            categories = [category.to_dict() for category in categories_obj]
            news = news_obj.to_dict()
            return render_template('news_edit_detail.html', news=news, categories=categories)
        else:
            news_info = request.form
            news_id = news_info.get('news_id')
            news = News.query.filter(News.id == news_id).first()
            news.title = news_info.get('title')
            news.digest = news_info.get('digest')
            new_category_id = news_info.get('category')
            news.category_id = new_category_id
            news.content = news_info.get('content')
            news.index_image_url = request.files.get('index_image_url')
            db.session.commit()
            return jsonify(errno=RET.OK, errmsg='修改成功')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


def news_type():
    """
    新闻分类的列表
    :return:
    """
    try:
        if request.method == 'GET':
            categories_obj = Category.query.all()
            categories = [category.to_dict() for category in categories_obj]
            return render_template('news_type.html', categories=categories)
        else:
            cate_info = request.json
            cate_name = request.json.get('name')
            if cate_info.get('id'):
                cate_id = request.json.get('id')
                category = Category.query.filter(Category.id == cate_id).first()
                category.name = cate_name
                db.session.commit()
                return jsonify(errno=RET.OK, errmsg='修改成功')
            else:
                new_category = Category()
                new_category.name = cate_name
                db.session.add(new_category)
                db.session.commit()
                return jsonify(errno=RET.OK, errmsg='添加成功')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
