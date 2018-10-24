from info.modules.admin import admin_blue
from info.modules.admin.login import login, index
from info.modules.admin.user_manager import user_count, user_list
from info.modules.admin.news_manager import news_review, review_detail
from info.modules.admin.news_manager import news_edit, edit_detail, news_type

admin_blue.route('/login', methods=['GET', 'POST'])(login)
admin_blue.route('/index', methods=['GET', 'POST'])(index)
admin_blue.route('/news_review')(news_review)
admin_blue.route('/review_detail', methods=['GET', 'POST'])(review_detail)
admin_blue.route('/news_edit')(news_edit)
admin_blue.route('/edit_detail', methods=['GET', 'POST'])(edit_detail)
admin_blue.route('/news_type', methods=['GET', 'POST'])(news_type)
admin_blue.route('/user_count')(user_count)
admin_blue.route('/user_list')(user_list)
