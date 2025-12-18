from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        Order.create(user_id=user_id, product_id=product_id)
        return redirect(url_for('order.index'))
    
    orders = Order.select().order_by(Order.created_at.desc())
    users = User.select()
    products = Product.select().order_by(Product.date)
    
    return render_template('order_list.html', 
                           orders=orders, 
                           users=users, 
                           products=products)