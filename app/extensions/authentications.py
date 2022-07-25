from flask_login import LoginManager
from app.dynamic_pgs.models import Users

login_manager = LoginManager()
login_manager.login_view = 'dynamic_pgs.login'

@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))