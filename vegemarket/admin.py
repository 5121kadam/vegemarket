from flask import Blueprint
from . import db
from .models import Category, ItemDetail

bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@bp.route('/dbseed')
def dbseed():
    category1 = Category(title = 'Vegitable', image = 'vegitable.jpg')
    category2 = Category(title = 'Fruit', image = 'fruit.jpg')
    
    try:
        db.session.add(category1)
        db.session.add(category2)
        db.session.commit()
    except:
        return 'There was an issue adding the Category in dbseed function'

    item1 = ItemDetail(item_id = category1.id, category = 'Vegitable', title = 'Tomato', description = 'Tomato Roma Red', image = 'Tomato.png', price = 5.00)
    item2 = ItemDetail(item_id = category1.id, category = 'Vegitable', title = 'Onion', description = 'Onion Red', image = 'Onion.png', price = 4.95)
    item3 = ItemDetail(item_id = category1.id, category = 'Vegitable', title = 'Lemon', description = 'Lemon Fresh', image = 'Lemon.png', price = 6.85)
    item4 = ItemDetail(item_id = category1.id, category = 'Vegitable', title = 'Cauliflower', description = 'Fresh Cauliflower', image = 'Cauliflower.png', price = 8.00)
    item5 = ItemDetail(item_id = category2.id, category = 'Fruit', title = 'Apple', description = 'Fresh Pink Lady Apples Each', image = 'Apple.png', price = 8.00)
    item6 = ItemDetail(item_id = category2.id, category = 'Fruit', title = 'Raspberries', description = 'Fresh Organic Raspberries', image = 'Black_raspberries.png', price = 6.00)
    item7 = ItemDetail(item_id = category2.id, category = 'Fruit', title = 'Orange', description = 'Fresh Orange Navel', image = 'Orange.png', price = 10.00)
    item8 = ItemDetail(item_id = category2.id, category = 'Fruit', title = 'Pomegranate', description = 'Spacial Fresh Pomegranate', image = 'Pomegranate.png', price = 7.00)
    item9 = ItemDetail(item_id = category2.id, category = 'Fruit', title = 'Papaya', description = 'Fresh Organic Papaya', image = 'Papaya.png', price = 5.00)
    item10 = ItemDetail(item_id = category2.id, category = 'Fruit', title = 'Plum', description = 'Fresh Organic Plum', image = 'Plum.png', price = 6.00)
    
    try:
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.add(item5)
        db.session.add(item6)
        db.session.add(item7)
        db.session.add(item8)
        db.session.add(item9)
        db.session.add(item10)

        db.session.commit()
    except:
        return 'There was an issue adding a item in dbseed function'

    return 'DATA LOADED'