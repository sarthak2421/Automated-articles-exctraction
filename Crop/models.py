from Crop import db
from Crop import bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Userdb, int(user_id))


class Userdb(db.Model,UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    uname = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)  # bcrypt hash is 60 chars
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Itemdb1', back_populates='owned_user', lazy=True)
    # backref : To identify a item belongs to which user.
    # lazy : To catch all query in one shot.
    # children = db.relationship("Item")
    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self,plain_txt_password):
        self.password = bcrypt.generate_password_hash(plain_txt_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        try:
            # Ensure consistent encoding/decoding
            attempted_password_encoded = attempted_password.encode('utf-8')
            return bcrypt.check_password_hash(self.password.encode('utf-8'), attempted_password_encoded)
        except Exception as e:
            print("Error occurred while checking password:", e)
            return False

    def can_purchase(self,p_obj):
        return self.budget >= p_obj.price

    def can_sell(self,s_obj):
        return s_obj in self.items

class Itemdb1(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    desc = db.Column(db.String(length=1024), nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('userdb.id'))
    owned_user = db.relationship('Userdb', back_populates='items', lazy=True)

    def buy(self, user):
        self.owner_id = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner_id = None
        user.budget += self.price
        db.session.commit()


