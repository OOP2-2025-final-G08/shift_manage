from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET', 'POST'])
def index():
    edit_id = request.args.get('edit')
    delete_id = request.args.get('delete')
    selected_user_id = request.args.get('user_id')

    # ===== 削除処理 =====
    if delete_id:
        order = Order.get_or_none(Order.id == delete_id)
        if order:
            order.delete_instance()
        return redirect(url_for('order.index'))

    # ===== 編集対象の取得 =====
    edit_order = None
    if edit_id:
        edit_order = Order.get_or_none(Order.id == edit_id)

    # ===== POST（追加 or 編集）=====
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        if order_id:
            # --- 編集 ---
            order = Order.get_by_id(order_id)
            order.user = request.form['user_id']
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

    # ===== 表示用データの準備 =====
    users = User.select()
    
    # 【除外ロジック】スタッフが選択されている場合、提出済みの枠を消す
    if selected_user_id:
        # そのスタッフが既に提出した枠のIDリスト
        submitted_product_ids = [
            o.product.id for o in Order.select().where(Order.user == selected_user_id)
        ]
        # 提出済みリストに入っていない枠だけを取得
        products = Product.select().where(Product.id.not_in(submitted_product_ids)).order_by(Product.date)
    else:
        # スタッフ未選択時は全枠を表示
        products = Product.select().order_by(Product.date)

    orders = Order.select().order_by(Order.created_at.desc())

    return render_template(
        'order_list.html',
        orders=orders,
        users=users,
        products=products,
        edit_order=edit_order,
        selected_user_id=selected_user_id
    )