from flask import Flask, render_template
from peewee import fn
from models import initialize_database, User, Product, Order
from routes import blueprints

app = Flask(__name__)

initialize_database()

for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/')
def index():
    # 1. サマリー (件数)
    total_users = User.select().count()
    total_products = Product.select().count()
    total_orders = Order.select().count()

    # 2. スタッフ(User)別 シフト希望提出回数ランキング
    user_ranking = (Order
                    .select(Order.user, fn.COUNT(Order.id).alias('count'))
                    .group_by(Order.user)
                    .order_by(fn.COUNT(Order.id).desc())
                    .limit(5))

    # 3. シフト枠(Product)別 人気倍率ランキング
    product_ranking = (Order
                       .select(Order.product, fn.COUNT(Order.id).alias('count'))
                       .group_by(Order.product)
                       .order_by(fn.COUNT(Order.id).desc())
                       .limit(5))

    # 4. 男女比率 (円グラフ用)
    gender_query = (User
                    .select(User.gender, fn.COUNT(User.id).alias('count'))
                    .group_by(User.gender))
    
    gender_labels = [row.gender if row.gender else '不明' for row in gender_query]
    gender_data = [row.count for row in gender_query]

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