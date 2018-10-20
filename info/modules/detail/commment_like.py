from flask import jsonify, request, g, current_app
from info.utils.commons import log_in_ifo
from info.response_code import *
from info.models import News, Comment, db, CommentLike


@log_in_ifo
def sub_comment():
    comment_info = request.json
    news_id = comment_info.get('news_id')
    comment_content = comment_info.get('comment')
    comment_parent_id = comment_info.get('parent_id') if comment_info.get('parent_id') else None
    try:
        news = News.query.filter(News.id == news_id).first()
        new_comment = Comment()
        new_comment.user_id = g.user.id
        new_comment.news_id = news_id
        new_comment.content = comment_content
        new_comment.parent_id = comment_parent_id
        news.comments.append(new_comment)
        db.session.commit()
        return jsonify(errno=RET.OK, errmsg='评论成功', data=new_comment.to_dict())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


@log_in_ifo
def show_like():
    comment_action = request.json
    comment_id = comment_action.get('comment_id')
    action = comment_action.get('action')
    if g.user:
        try:
            comment = Comment.query.get(comment_id)
            if action == 'add':
                comment.like_count += 1
                comment_like = CommentLike()
                comment_like.user_id = g.user.id
                comment_like.comment_id = comment_id
                g.user.comment_likes.append(comment_like)
                db.session.commit()
            else:
                comment_like = CommentLike.query.filter(CommentLike.user_id == g.user.id,
                                                        CommentLike.comment_id == comment_id).first()
                db.session.delete(comment_like)
                comment.like_count -= 1
                db.session.commit()
            return jsonify(errno=RET.OK, errmsg='操作成功')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    else:
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.OK])
