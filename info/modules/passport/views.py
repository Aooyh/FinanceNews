from info.modules.passport import passport_blue
from info.modules.passport.logout import logout
from info.modules.passport.login import login
from info.modules.passport.register import *

passport_blue.route('/register', methods=['post'])(register)
passport_blue.route('/image_code')(get_image_code)
passport_blue.route('/sms_code', methods=['post'])(get_sms_code)
passport_blue.route('/login', methods=['post'])(login)
passport_blue.route('/logout', methods=['post'])(logout)
