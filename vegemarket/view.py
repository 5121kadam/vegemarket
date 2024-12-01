from flask import Blueprint, render_template, session, redirect, flash, url_for, request
from datetime import datetime
from .models import Category, ItemDetail, Card 
from .forms import CheckoutForm
from . import db

bp = Blueprint('main',__name__)

@bp.route('/')
def index():
    item_list = db.session.scalars(db.select(Category).order_by(Category.id)).all()
    return render_template('index.html', items = item_list)

@bp.route('/item_list/<int:categorytitle>', methods = ['POST','GET'])
def itemlist(categorytitle):
    item_details = db.session.scalars(db.select(ItemDetail).where(ItemDetail.item_id==categorytitle)).all()
    if categorytitle == 1:
        return render_template('itemlist.html',category = 'Vegitable', items = item_details)
    else:
        return render_template('itemlist.html',category = 'Fruit', items = item_details)

# Item Detail Navigation with selected item Data
@bp.route('/detail/<int:itemid>', methods = ['POST','GET'])
def itemdetail(itemid):
    selecteditem = db.session.scalars(db.select(ItemDetail).where(ItemDetail.id==itemid)).all()

    return render_template('detail.html', itemDetail = selecteditem)

# BASKET Navigation
@bp.route('/cart/', methods=['POST', 'GET'])
def cart():
    itemdetail_id = request.values.get('itemdetail_id')
    # retrieve order if there is one
    if 'order_id' in session.keys():
        cartdetail = db.session.scalar(db.select(Card).where(Card.id==session['order_id']))
    else:
        cartdetail = None

    # create new order if needed
    if cartdetail is None:
        cartdetail = Card(status=False, first_name='', surname='', email='', phone='', total_cost=0, date=datetime.now())
        try:
            db.session.add(cartdetail)
            db.session.commit()
            session['order_id'] = cartdetail.id
        except:
            print('Failed trying to create a new order!')
            cartdetail = None
    
    # calculate total price
    total_price = 0
    if cartdetail is not None:
        for cartproducts in cartdetail.item_detail:
            total_price += float(cartproducts.price)
    
    # are we adding an item?
    if itemdetail_id is not None and cartdetail is not None:
        basketproducts = db.session.scalar(db.select(ItemDetail).where(ItemDetail.id==itemdetail_id))
        if basketproducts not in cartdetail.item_detail:
            try:
                cartdetail.item_detail.append(basketproducts)
                db.session.commit()
            except:
                flash('There was an issue adding the item to your cart',category='danger')
            return redirect(url_for('main.cart'))
        else:
            flash('There is already one of these in the cart')
            return redirect(url_for('main.cart'))
    return render_template('cart.html', basketitems=cartdetail.item_detail, total_price=total_price)

@bp.route('/deletecartitem/<int:id>', methods=['POST','GET'])
def deletecartitem(id):
    if 'order_id' in session:
        cart = db.get_or_404(Card, session['order_id'])
        product_to_delete = db.session.scalar(db.select(ItemDetail).where(ItemDetail.id==id))
        try:
            cart.item_detail.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.cart'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.cart'))

@bp.route('/deletecart/')
def deletecart():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.cart'))

@bp.route('/checkout/', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = db.get_or_404(Card, session['order_id'])
        if form.validate_on_submit():
            order.status = True
            order.first_name = form.firstName.data
            order.surname = form.lastName.data
            order.email = form.email.data
            order.phone = form.phone.data
            total_cost = 0
            for productdetail in order.item_detail:
                total_cost += productdetail.price
            order.total_cost = total_cost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)

# Search Item 
# def search():
#     search = request.args.get('search')
#     search = '%{}%'.format(search) 
#     itemlists = ItemDetail.query.filter(ItemDetail.description.like(search)).all()
#     if itemlists is not None:
#         item_list = db.session.scalars(db.select(Category).order_by(Category.id)).all()
#         return render_template('index.html', items = item_list)
#     return render_template('searchlist.html', itemlist=itemlists)


@bp.route('/searchitem/')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    item_list = ItemDetail.query.filter(ItemDetail.title.like(search)).all()
    return render_template('searchlist.html', itemlist=item_list)