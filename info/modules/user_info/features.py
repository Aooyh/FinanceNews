from flask import render_template, g, request, current_app, jsonify, redirect
from info.utils.commons import log_in_ifo
from info.constants import QINIU_DOMIN_PREFIX
from info.utils.image_storge import image_storage
from info.models import db, Category, News, User
from info.response_code import *


@log_in_ifo
def user_info():
    """
    若用户未登录, 无法访问用户页面
    :return:
    """
    if not g.user:
        redirect('/')
    return render_template('user.html', user_info=g.user_info)


@log_in_ifo
def basic_info():
    """
    修改用户的基本信息
    :return:
    """
    if request.method == 'GET':
        return render_template('user_base_info.html', user_info=g.user_info)
    else:
        try:
            new_basic_info = request.json
            g.user.signature = new_basic_info.get('signature')
            g.user.nick_name = new_basic_info.get('nick_name')
            g.user.gender = new_basic_info.get('gender')
            db.session.commit()
            return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def pic_change():
    """
    修改用户头像
    :return:
    """
    if request.method == 'GET':
        return render_template('user_pic_info.html', user_info=g.user_info)
    else:
        try:
            new_picture = request.files.get('avatar')
            if new_picture:
                new_picture_url = QINIU_DOMIN_PREFIX + image_storage(new_picture.read())
                g.user.avatar_url = new_picture_url
                db.session.commit()
                return jsonify(errno=RET.OK, errmsg='上传成功', avatar_url=new_picture_url)
            else:
                return jsonify(errno=RET.DATAEXIST, errmsg='请上传头像')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def user_follower():
    """
    用户关注的信息及修改
    :return:
    """
    if request.method == 'GET':
        try:
            request_page = int(request.args.get('p', '1'))
            paginate = g.user.followed.paginate(request_page, 4, False)
            followeds = paginate.items
            current_page = paginate.page
            total_page = paginate.pages
            followed_list = [followed.to_dict() for followed in followeds]
            return render_template('user_follow.html', user_info=g.user_info, followed_list=followed_list,
                                   currentPage=current_page, totalPage=total_page)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    else:
        try:
            follow_info = request.json
            user_id = follow_info.get('user_id')
            followed_user = User.query.filter(User.id == user_id).first()
            action = follow_info.get('action')
            if action == 'unfollow':
                followed_user.followers.remove(g.user)
                db.session.commit()
                return jsonify(errno=RET.OK, errmsg='取消关注成功')
            else:
                followed_user.followers.append(g.user)
                db.session.commit()
                return jsonify(errno=RET.OK, errmsg='关注成功')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def passwd_change():
    """
    用户密码修改
    :return:
    """
    if request.method == 'GET':
        return render_template('user_pass_info.html')
    else:
        try:
            passwd_info = request.json
            old_password = passwd_info.get('old_password')
            new_password = passwd_info.get('new_password')
            if g.user.check_passowrd(old_password):
                g.user.password = new_password
                db.session.commit()
                return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])
            else:
                return jsonify(errno=RET.DATAERR, errmsg='旧密码错误')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def user_collect():
    """
    用户收藏新闻的展示及更改
    :return:
    """
    try:
        page = request.args.get('p', 1)
        paginate = g.user.collection_news.paginate(int(page), 4, False)
        total_page = paginate.pages
        current_page = paginate.page
        collections = paginate.items
        collection_list = [collection.to_dict() for collection in collections]
        return render_template('user_collection.html', collection_list=collection_list,
                               totalPage=total_page, currentPage=current_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def news_release():
    """
    用户发布新闻
    :return:
    """
    try:
        if request.method == 'GET':
            categories = Category.query.filter(Category.id > 1).all()
            category_list = [category.to_dict() for category in categories]
            return render_template('user_news_release.html', category_list=category_list)
        else:
            news_info = request.form
            new_news = News()
            new_news.category_id = news_info.get('category_id')
            new_news.content = news_info.get('content')
            new_news.digest = news_info.get('digest')
            new_news.title = news_info.get('title')
            new_news.source = g.user.nick_name
            new_news.user_id = g.user.id
            image_url = request.files.get('index_image')
            if not image_url:
                return jsonify(errno=RET.NODATA, errmsg='没有上传图片')
            else:
                try:
                    new_news.index_image_url = QINIU_DOMIN_PREFIX + image_storage(image_url.read())
                except Exception as e:
                    current_app.logger.error(e)
                    return jsonify(errno=RET.THIRDERR, errmsg=error_map[RET.THIRDERR])
            db.session.add(new_news)
            db.session.commit()
            return jsonify(errno=RET.OK, errmsg='发表成功')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def user_news():
    """
    用户发布的新闻列表
    :return:
    """
    try:
        if not request.args.get('user_id'):
            page = int(request.args.get('p', '1'))
            paginate = News.query.filter(News.source == g.user.nick_name).paginate(page, 4, False)
            news_obj_list = paginate.items
            current_page = paginate.page
            total_page = paginate.pages
            news_list = [news.to_review_dict() for news in news_obj_list]
            return render_template('user_news_list.html', newsList=news_list,
                                   currentPage=current_page, totalPage=total_page)
        else:
            page = int(request.args.get('p', '1'))
            user_id = request.args.get('user_id')
            user = User.query.get(user_id)
            paginate = News.query.filter(News.source == user.nick_name).paginate(page, 4, False)
            news_obj_list = paginate.items
            current_page = paginate.page
            total_page = paginate.pages
            news_list = [news.to_review_dict() for news in news_obj_list]
            return jsonify(errno=RET.OK, newsList=news_list, currentPage=current_page, totalPage=total_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def others(user_id):
    """
    其他用户页面请求
    :param user_id:
    :return:
    """
    author_obj = User.query.get(user_id)
    author = author_obj.to_dict()
    if g.user:
        if author_obj in g.user.followed:
            author['is_followed'] = True
    return render_template('other.html', user_info=g.user_info, author=author)
