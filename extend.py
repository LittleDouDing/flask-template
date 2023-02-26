from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_mail import Mail
from flask_apscheduler import APScheduler

mail = Mail()
cors = CORS()
scheduler = APScheduler()
limiter = Limiter(key_func=get_remote_address, default_limits=["10000 per day", "1000/hour"])
