from info.modules.detail import detail_blue
from info.modules.detail.user_collect import user_collect
from info.modules.detail.news_detail import news_detail, follow
from info.modules.detail.commment_like import sub_comment, show_like

detail_blue.route('/<int:news_id>')(news_detail)
detail_blue.route('/news_collect', methods=['POST'])(user_collect)
detail_blue.route('/news_comment', methods=['POST'])(sub_comment)
detail_blue.route('/comment_like', methods=['POST'])(show_like)
detail_blue.route('/follow', methods=['POST'])(follow)
