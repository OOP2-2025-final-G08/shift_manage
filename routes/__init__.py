from .user_routes import user_bp
from .product_routes import product_bp
from .order_routes import order_bp

# app.pyで登録するためのリスト
blueprints = [
    user_bp,
    product_bp,
    order_bp,
]