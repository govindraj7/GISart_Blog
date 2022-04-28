from app.app import create_app
from app.dynamic_pgs.models import Users
from app.extensions.database import db

app = create_app()
app.app_context().push()

user_data = {
  'chocolate-chip' : {'user_name': 'ChocolateChip', 'first_name': 'Chocolate', 'last_name': 'Chip', 'email': 'cookie@dough.com'},
  'bizkut' : {'user_name': 'Cbizkut', 'first_name': 'firstnamehere', 'last_name': 'Lastnamehere', 'email': 'bizkut@party.com'}
}

for slug, user in user_data.items():
  new_user = Users(slug=slug, user_name=user['user_name'], first_name=user['first_name'], last_name=user['last_name'],  email=user['email'])
  db.session.add(new_user)

db.session.commit()
