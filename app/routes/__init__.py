from .auth import auth_bp
from .health import health_bp
from .inventory import inventory_bp
from .products import products_bp
from .stock import stock_bp
from .warehouses import warehouses_bp


def register_routes(app):
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(warehouses_bp, url_prefix="/api")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(stock_bp, url_prefix="/api")

