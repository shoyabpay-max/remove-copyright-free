
import os
import hmac
import hashlib
import uuid
import razorpay

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

client = None
if KEY_ID and KEY_SECRET:
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

PLAN_AMOUNT = 4900  # ₹49 in paise


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Razorpay backend is running"
    })


@app.route("/api/create-order", methods=["POST"])
def create_order():
    if not client:
        return jsonify({"error": "Payment service not configured"}), 500

    try:
        order = client.order.create({
            "amount": PLAN_AMOUNT,
            "currency": "INR",
            "receipt": "starter_" + uuid.uuid4().hex[:20]
        })

        return jsonify({
            "key_id": KEY_ID,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]
        })

    except Exception:
        app.logger.exception("Order creation failed")
        return jsonify({"error": "Could not create order"}), 500


@app.route("/api/verify-payment", methods=["POST"])
def verify_payment():
    if not client:
        return jsonify({"error": "Payment service not configured"}), 500

    data = request.get_json(silent=True) or {}
    order_id = data.get("razorpay_order_id", "")
    payment_id = data.get("razorpay_payment_id", "")
    signature = data.get("razorpay_signature", "")

    if not all([order_id, payment_id, signature]):
        return jsonify({"error": "Missing payment details"}), 400

    message = f"{order_id}|{payment_id}"
    expected = hmac.new(
        KEY_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        return jsonify({"verified": False, "error": "Invalid signature"}), 400

    try:
        payment = client.payment.fetch(payment_id)

        if payment.get("order_id") != order_id:
            return jsonify({"verified": False, "error": "Order mismatch"}), 400

        if (
            payment.get("amount") != PLAN_AMOUNT
            or payment.get("currency") != "INR"
        ):
            return jsonify({"verified": False, "error": "Amount mismatch"}), 400

        if payment.get("status") != "captured":
            return jsonify({
                "verified": False,
                "status": payment.get("status"),
                "message": "Payment is not captured yet"
            }), 400

        return jsonify({
            "verified": True,
            "message": "Payment verified successfully"
        })

    except Exception:
        app.logger.exception("Payment verification failed")
        return jsonify({"error": "Could not verify payment"}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
