from flask import Flask, request, render_template
import sqlite3
import os
from flask import redirect
from db import get_order_counts, update_status
from twilio.rest import Client
from db import get_products, save_order
from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from db import init_db, save_order, get_all_orders

app = Flask(__name__)
init_db()

user_state = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    phone = request.form.get("From")
    msg = request.form.get("Body","").strip().lower()
    resp = MessagingResponse()

    if phone not in user_state:
        user_state[phone] = {}

    if msg in ["hi","hello"]:
        resp.message("Welcome 👋\n1. View Products\n2. Place Order\n3. Contact Farmer")

    elif msg == "1":
     resp.message(
         "🛒 View all fruits & vegetables with images:\n"
         "👉 https://alexander-garnishable-regretfully.ngrok-free.dev/catalog"
    )


    elif msg == "2":
        user_state[phone]["step"] = "product"
        resp.message("Enter product name")

    elif user_state[phone].get("step") == "product":
        user_state[phone]["product"] = msg
        user_state[phone]["step"] = "quantity"
        resp.message("Enter quantity")

    elif user_state[phone].get("step") == "quantity":
        try:
            quantity = int(msg)
            product = user_state[phone]["product"]
            save_order(phone, product, quantity)
            user_state[phone] = {}
            resp.message(f"✅ Order Confirmed\nProduct: {product}\nQuantity: {quantity}")
        except:
            resp.message("Please enter a valid number")

    elif msg == "3":
        resp.message("📞 Contact: 9381400894")

    else:
        resp.message("Invalid option. Reply Hi to start.")

    return str(resp)

@app.route("/catalog")
def catalog():
    products = get_products()
    return render_template("catalog.html", products=products)

@app.route("/place_order", methods=["POST"])
def place_order():
    product = request.form["product"]
    quantity = request.form["quantity"]
    save_order("WEB_USER", product, quantity)
    return "✅ Order placed successfully. You may close this page."


@app.route("/admin")
def admin():
    orders = get_all_orders()
    total, confirmed, delivered = get_order_counts()
    return render_template(
        "admin.html",
        orders=orders,
        total=total,
        confirmed=confirmed,
        delivered=delivered
    )

@app.route("/update_status/<int:order_id>")
def update_status_route(order_id):
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()

    cur.execute("SELECT phone, product FROM orders WHERE id=?", (order_id,))
    row = cur.fetchone()

    if row:
        phone, product = row
        cur.execute("UPDATE orders SET status='DELIVERED' WHERE id=?", (order_id,))
        conn.commit()

        if phone.startswith("whatsapp:"):
            send_delivery_message(phone, product)

    conn.close()
    return redirect("/admin")


ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP = "whatsapp:+14155238886"


def send_delivery_message(to_number, product):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        from_=TWILIO_WHATSAPP,
        to=to_number,
        body=f"✅ Your order for {product} has been delivered. Thank you for shopping with us!"
    )




if __name__ == "__main__":
    app.run()
