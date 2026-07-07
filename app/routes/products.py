from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import Product


products_bp = Blueprint("products", __name__)


def product_to_dict(product):
    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "unit": product.unit,
        "low_stock_threshold": product.low_stock_threshold,
        "is_active": product.is_active,
    }


@products_bp.get("")
@jwt_required()
def list_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return jsonify([product_to_dict(product) for product in products])


@products_bp.post("")
@jwt_required()
def create_product():
    data = request.get_json() or {}
    if not data.get("sku") or not data.get("name"):
        return jsonify({"error": "sku_and_name_required"}), 400

    product = Product(
        sku=data["sku"],
        name=data["name"],
        unit=data.get("unit") or "pcs",
        low_stock_threshold=int(data.get("low_stock_threshold") or 0),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product_to_dict(product)), 201


@products_bp.get("/<int:product_id>")
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_to_dict(product))


@products_bp.put("/<int:product_id>")
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}

    for field in ["sku", "name", "unit", "is_active"]:
        if field in data:
            setattr(product, field, data[field])
    if "low_stock_threshold" in data:
        product.low_stock_threshold = int(data["low_stock_threshold"])

    db.session.commit()
    return jsonify(product_to_dict(product))


@products_bp.delete("/<int:product_id>")
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    return jsonify({"deleted": True})

