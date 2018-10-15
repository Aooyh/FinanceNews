from info.modules.passport import passport_blue
from info.modules.passport.logout import *
from info.modules.passport.login import *
from info.modules.passport.register import *

passport_blue.route('/register')(register)
passport_blue.route('/image_code')(image_code)
passport_blue.route('/sms_code')(sms_code)
passport_blue.route('/login')(login)
passport_blue.route('/logout')(logout)
