from flask import Blueprint, render_template, request, redirect, url_for
from models import Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        time_range = request.form['time_range']
        Product.create(date=date, name=time_range, price=1000)
        return redirect(url_for('product.index'))
    
    products = Product.select().order_by(Product.date)
    return render_template('product_list.html', products=products)