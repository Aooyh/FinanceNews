from info.modules.user_info import user_info_blue
from info.modules.user_info.features import *

user_info_blue.route('/user_info')(user_info)
user_info_blue.route('/basic_info', methods=['GET', 'POST'])(basic_info)
user_info_blue.route('/picture_info', methods=['GET', 'POST'])(pic_change)
user_info_blue.route('/follow_info', methods=['GET', 'POST'])(user_follower)
user_info_blue.route('/pass_info', methods=['GET', 'POST'])(passwd_change)
user_info_blue.route('/news_release', methods=['GET', 'POST'])(news_release)
user_info_blue.route('/collect_info', methods=['GET'])(user_collect)
user_info_blue.route('/news_info', methods=['GET'])(user_news)
user_info_blue.route('/other_info/<int:user_id>', methods=['GET'])(others)
