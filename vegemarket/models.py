from . import db

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    image = db.Column(db.String(60), nullable=False, default = 'defaultcity.jpg')
    item_detail = db.relationship('ItemDetail', backref='Category', cascade="all, delete-orphan")

class ItemDetail(db.Model):
    __tablename__ = 'item_details'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultimage.jpg')
    price = db.Column(db.Float)
    item_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))

carddetails = db.Table('carddetails', 
    db.Column('card_id',db.Integer,db.ForeignKey('cards.id'),nullable=False),
    db.Column('itemdetails_id', db.Integer,db.ForeignKey('item_details.id'), nullable=False),
    db.PrimaryKeyConstraint('card_id', 'itemdetails_id') )


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    total_cost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    item_detail = db.relationship("ItemDetail", secondary='carddetails', backref="cards")
 