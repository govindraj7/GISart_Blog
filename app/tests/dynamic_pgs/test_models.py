from app.extensions.database import db, CRUDMixin
from app.dynamic_pgs.models import Users

def test_user_update(Users):
  # updates cookie's properties
  user = Users(slug='testing', user_name='Name')
  db.session.add(user)
  db.session.commit()

  user.user_name='Changed'
  user.save()

  updated_user = Users.query.filter_by(slug='testing').first()
  assert updated_user.user_ame == 'Changed'

# todo: sort out this CRUDMixin shizzzz