# booking.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
import uuid

from .store import bookings
from .auth import require_admin

booking_bp = Blueprint("booking", __name__)

@booking_bp.post("/bookings")
@jwt_required()
def create_booking():
    username = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    slot = data.get("slot")

    if not slot or not isinstance(slot, str):
        return jsonify({"error": "slot (string) required"}), 400

    booking_id = str(uuid.uuid4())
    booking = {"id": booking_id, "owner": username, "slot": slot}
    bookings[booking_id] = booking
    return jsonify(booking), 201


@booking_bp.get("/bookings")
@jwt_required()
def list_bookings():
    username = get_jwt_identity()
    is_admin = get_jwt().get("is_admin", False)

    if is_admin:
        return jsonify(list(bookings.values()))
    return jsonify([b for b in bookings.values() if b["owner"] == username])


@booking_bp.put("/bookings/<booking_id>")
@jwt_required()
def update_booking(booking_id):
    username = get_jwt_identity()
    is_admin = get_jwt().get("is_admin", False)

    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if (not is_admin) and booking["owner"] != username:
        return jsonify({"error": "Not allowed"}), 403

    data = request.get_json(silent=True) or {}
    slot = data.get("slot")
    if not slot or not isinstance(slot, str):
        return jsonify({"error": "slot (string) required"}), 400

    booking["slot"] = slot
    return jsonify(booking), 200


@booking_bp.delete("/bookings/<booking_id>")
@jwt_required()
def delete_booking(booking_id):
    username = get_jwt_identity()
    is_admin = get_jwt().get("is_admin", False)

    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if (not is_admin) and booking["owner"] != username:
        return jsonify({"error": "Not allowed"}), 403

    del bookings[booking_id]
    return jsonify({"deleted": booking_id})


@booking_bp.get("/admin/bookings")
@jwt_required()
def admin_list_all_bookings():
    admin_check = require_admin()
    if admin_check:
        return admin_check
    return jsonify(list(bookings.values()))