from flask import render_template, current_app, jsonify
from flask import request
from info.response_code import *
from info.models import User
from datetime import timedelta, datetime
import time


def user_count():
    try:
        all_user = User.query.filter(User.is_admin == 0)
        total_count = all_user.count()
        calender = time.localtime()
        mon_start_str = '%d-%d-01' % (calender.tm_year, calender.tm_mon)
        day_start_str = '%d-%d-%d' % (calender.tm_year, calender.tm_mon, calender.tm_mday)
        mon_start_time = datetime.strptime(mon_start_str, '%Y-%m-%d')
        day_start_time = datetime.strptime(day_start_str, '%Y-%m-%d')
        mon_create_count = all_user.filter(User.create_time >= mon_start_time).count()
        day_create_count = all_user.filter(User.create_time >= day_start_time).count()
        mon_count = list()
        active_count = list()
        for i in range(31):
            start_date = day_start_time - timedelta(days=i)
            end_date = day_start_time - timedelta(days=i-1)
            mon_count.append(start_date.strftime('%m-%d'))
            active_user = all_user.filter(User.last_login >= start_date, User.last_login <= end_date).count()
            active_count.append(active_user)
        mon_count.reverse()
        active_count.reverse()
        data = {
            'total_count': total_count,
            'mon_create_count': mon_create_count,
            'day_create_count': day_create_count,
            'mon_count': mon_count,
            'active_count': active_count
        }
        return render_template('user_count.html', data=data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])


def user_list():
    try:
        page = int(request.args.get('p', '1'))
        pagniate = User.query.filter(User.is_admin == 0).paginate(page, 10, False)
        users_obj = pagniate.items
        users = [user.to_admin_dict() for user in users_obj]
        current_page = pagniate.page
        total_page = pagniate.pages
        data = {
            'users': users,
            'current_page': current_page,
            'total_page': total_page
        }
        return render_template('user_list.html', data=data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
