from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET', 'POST'])
def index():
    edit_id = request.args.get('edit')
    delete_id = request.args.get('delete')

    selected_user_id = request.args.get('user_id')

    # ===== 削除 =====
    if delete_id:
        order = Order.get_or_none(Order.id == delete_id)
        if order:
            order.delete_instance()
        return redirect(url_for('order.index'))

    # ===== 編集対象 =====
    edit_order = None
    if edit_id:
        edit_order = Order.get_or_none(Order.id == edit_id)

    # ===== POST（追加 or 編集）=====
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        if order_id:
            # --- 編集 ---
            order = Order.get_by_id(order_id)

            # スタッフ変更
            order.user = request.form['user_id']

            # 時間変更
            new_time = request.form['product_name']
            product = order.product
            product.name = new_time
            product.save()

            order.save()
        else:
            # --- 新規提出 ---
            user_id = request.form['user_id']
            product_id = request.form['product_id']
            Order.create(user_id=user_id, product_id=product_id)

        return redirect(url_for('order.index'))

    orders = Order.select().order_by(Order.created_at.desc())
    users = User.select()
    products = Product.select().order_by(Product.date)

    # 選択されたスタッフのIDを取得（URLパラメータにある場合）
    selected_user_id = request.args.get('user_id')
    
    if selected_user_id:
        # そのスタッフが既に提出した product_id のリストを取得
        submitted_product_ids = [
            o.product.id for o in Order.select().where(Order.user == selected_user_id)
        ]
        # まだ提出していない枠だけをフィルタリング
        products = Product.select().where(Product.id.not_in(submitted_product_ids))
    else:
        # スタッフが選ばれていない時は全件（または空）
        products = Product.select()

    # ...以下、render_template で products を渡す...

    orders = Order.select().order_by(Order.created_at.desc())

    return render_template(
        'order_list.html',
        orders=orders,
        users=users,
        products=products,
        edit_order=edit_order,
        selected_user_id=selected_user_id
    )