from flask import Flask, render_template, jsonify
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
    return render_template('index.html')

# APIルート：ここですべての統計データを今月分に絞って返す
@app.route('/api/stats')
def get_stats():
    today = date.today()
    first_day = today.replace(day=1).isoformat()
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1]).isoformat()

    # 今月のサマリー
    totals = {
        "users": User.select().count(),
        "products": Product.select().where(Product.name.between(first_day, last_day)).count(),
        "orders": Order.select().join(Product).where(Product.name.between(first_day, last_day)).count()
    }

    # スタッフ別ランキング (今月)
    user_ranking = list(User.select(User.name, fn.COUNT(Order.id).alias('count'))
                        .join(Order, on=(User.id == Order.user))
                        .join(Product, on=(Order.product == Product.id))
                        .where(Product.name.between(first_day, last_day))
                        .group_by(User.id)
                        .order_by(fn.COUNT(Order.id).desc()).limit(5).dicts())

    # 人気シフト枠ランキング (今月)
    product_ranking = list(Product.select(Product.name, Product.name.alias('date'), fn.COUNT(Order.id).alias('count'))
                           .join(Order, on=(Product.id == Order.product))
                           .where(Product.name.between(first_day, last_day))
                           .group_by(Product.id)
                           .order_by(fn.COUNT(Order.id).desc()).limit(5).dicts())

    # 男女比率
    gender_query = list(User.select(User.gender, fn.COUNT(User.id).alias('count')).group_by(User.gender).dicts())
    gender = {
        "labels": [g['gender'] for g in gender_query],
        "values": [g['count'] for g in gender_query]
    }

    return jsonify({
        "month": today.strftime('%Y年%m月'),
        "totals": totals,
        "user_ranking": user_ranking,
        "product_ranking": product_ranking,
        "gender": gender
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)