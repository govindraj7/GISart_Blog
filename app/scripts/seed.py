from app.app import create_app
from app.dynamic_pgs.models import Users
from app.extensions.database import db

app = create_app()
app.app_context().push()

user_data = {
  'CookieCream' : {'user_name': 'Cookes&Cream', 'first_name': 'Tercera Valencia', 'last_name': 'Hernández González', 'email': 'hernandez@gg.com'},
}

for slug, user in user_data.items():
  new_user = Users(slug=slug, user_name=user['user_name'], first_name=user['first_name'], last_name=user['last_name'],  email=user['email'])
  db.session.add(new_user)

db.session.commit()
