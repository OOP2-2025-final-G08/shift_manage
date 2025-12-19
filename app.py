from flask import Flask, render_template
from peewee import fn
from models import initialize_database, User, Product, Order
from routes import blueprints
from datetime import date
import calendar

app = Flask(__name__)
initialize_database()

for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/')
def index():
    # 今月（2025年12月）の範囲を計算
    today = date.today()
    first_day = today.replace(day=1).isoformat()
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1]).isoformat()

    # サマリー件数
    total_users = User.select().count()
    total_products = Product.select().count()
    total_orders = Order.select().count()

    # 1. スタッフ別提出回数 (今月) - 同順位対応のため全件取得しHTMLへ渡す
    user_ranking = (Order
                    .select(Order.user, fn.COUNT(Order.id).alias('count'))
                    .join(Product)
                    .where(Product.date.between(first_day, last_day))
                    .group_by(Order.user)
                    .order_by(fn.COUNT(Order.id).desc()))

    # 2. 人気シフト枠 (今月)
    product_ranking = (Order
                       .select(Order.product, fn.COUNT(Order.id).alias('count'))
                       .join(Product)
                       .where(Product.date.between(first_day, last_day))
                       .group_by(Order.product)
                       .order_by(fn.COUNT(Order.id).desc()))

    # 3. 男女比率
    gender_query = (User.select(User.gender, fn.COUNT(User.id).alias('count')).group_by(User.gender))
    gender_dict = {row.gender: row.count for row in gender_query}
    # gender_labels = [row.gender if row.gender else '不明' for row in gender_query]
    # gender_data = [row.count for row in gender_query]
    gender_labels = ['男性', '女性']
    gender_data = [
        gender_dict.get('男性', 0), 
        gender_dict.get('女性', 0)
    ]

    return render_template('index.html',
                           total_users=total_users,
                           total_products=total_products,
                           total_orders=total_orders,
                           user_ranking=user_ranking,
                           product_ranking=product_ranking,
                           gender_labels=gender_labels,
                           gender_data=gender_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)