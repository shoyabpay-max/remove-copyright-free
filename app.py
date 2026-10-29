
import os
import razorpay
from flask import Flask, jsonify, request

app = Flask(__name__)

KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

client = None
if KEY_ID and KEY_SECRET:
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Razorpay backend is running"
    })


@app.route("/api/create-order", methods=["POST"])
def create_order():
    if not client:
        return jsonify({"error": "Razorpay keys not configured"}), 500

    data = request.get_json(silent=True) or {}

    try:
        amount = int(data.get("amount", 0))

        if amount < 100 or amount > 1000000:
            return jsonify({"error": "Invalid amount"}), 400

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": "receipt_demo_001"
        })

        return jsonify({
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": KEY_ID
        })

    except Exception:
        app.logger.exception("Order creation failed")
        return jsonify({"error": "Order creation failed"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
