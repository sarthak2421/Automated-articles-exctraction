from Crop.models import db, Userdb, Itemdb1
from Crop.routes import app

app.app_context().push()
# Create a new user
#user1 = Userdb(uname='abc', email='abc12@gmail.com', password='12345abc', budget=700)

# Create a new item
item1 = Itemdb1(name='VIVO', barcode='12332111360', price=499, desc='VIVO V30')

# Add the user and item to the session
#db.session.add(user1)
db.session.add(item1)

# Commit the changes to the database
db.session.commit()