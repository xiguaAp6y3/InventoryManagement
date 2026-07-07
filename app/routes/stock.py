from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import StockInOrder, StockMovement, StockOutOrder
from ..services.stock_service import apply_stock_in, apply_stock_out


stock_bp = Blueprint("stock", __name__)


def order_to_dict(order):
    return {
        "id": order.id,
        "order_no": order.order_no,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "warehouse_id": item.warehouse_id,
                "location_id": item.location_id,
                "quantity": item.quantity,
            }
            for item in order.items
        ],
    }


@stock_bp.post("/stock-in")
@jwt_required()
def stock_in():
    try:
        order = apply_stock_in(request.get_json() or {})
        return jsonify(order_to_dict(order)), 201
    except (KeyError, TypeError, ValueError) as exc:
        db.session.rollback()
        return jsonify({"error": str(exc)}), 400


@stock_bp.get("/stock-in")
@jwt_required()
def list_stock_in():
    orders = StockInOrder.query.order_by(StockInOrder.id.desc()).limit(100).all()
    return jsonify([order_to_dict(order) for order in orders])


@stock_bp.get("/stock-in/<int:order_id>")
@jwt_required()
def get_stock_in(order_id):
    order = StockInOrder.query.get_or_404(order_id)
    return jsonify(order_to_dict(order))


@stock_bp.post("/stock-out")
@jwt_required()
def stock_out():
    try:
        order = apply_stock_out(request.get_json() or {})
        return jsonify(order_to_dict(order)), 201
    except (KeyError, TypeError, ValueError) as exc:
        db.session.rollback()
        return jsonify({"error": str(exc)}), 400


@stock_bp.get("/stock-out")
@jwt_required()
def list_stock_out():
    orders = StockOutOrder.query.order_by(StockOutOrder.id.desc()).limit(100).all()
    return jsonify([order_to_dict(order) for order in orders])


@stock_bp.get("/stock-out/<int:order_id>")
@jwt_required()
def get_stock_out(order_id):
    order = StockOutOrder.query.get_or_404(order_id)
    return jsonify(order_to_dict(order))


@stock_bp.get("/stock-movements")
@jwt_required()
def list_stock_movements():
    query = StockMovement.query
    product_id = request.args.get("product_id")
    if product_id:
        query = query.filter_by(product_id=int(product_id))

    rows = query.order_by(StockMovement.id.desc()).limit(200).all()
    return jsonify(
        [
            {
                "id": row.id,
                "movement_type": row.movement_type,
                "reference_no": row.reference_no,
                "product_id": row.product_id,
                "warehouse_id": row.warehouse_id,
                "location_id": row.location_id,
                "quantity_delta": row.quantity_delta,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    )

