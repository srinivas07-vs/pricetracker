from flask import Flask, render_template, request
import json
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# -------------------------------
# LOAD PRICES
# -------------------------------
def load_prices():
    if os.path.exists("prices.json"):
        with open("prices.json", "r") as file:
            return json.load(file)
    return {}

# -------------------------------
# SAVE PRICES
# -------------------------------
def save_prices(data):
    with open("prices.json", "w") as file:
        json.dump(data, file)

# -------------------------------
# SEND EMAIL
# -------------------------------
def send_email(product, old_price, new_price):
    sender = "vadlapudisrinivas30@gmail.com"
    receiver = "bsujithbsujith53@gmail.com.com"
    password = "ptabokjrtecoqigj"

    message = f"{product} price dropped from ₹{old_price} to ₹{new_price}!"

    msg = MIMEText(message)
    msg["Subject"] = "Price Drop Alert!"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

# -------------------------------
# MAIN ROUTE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    old_price = None

    if request.method == "POST":
        product = request.form["product"]
        current_price = int(request.form["price"])

        prices = load_prices()

        if product in prices:
            old_price = prices[product]

            if current_price < old_price:
                message = "🔥 Price Dropped! Email Sent!"
                send_email(product, old_price, current_price)

            elif current_price > old_price:
                message = "📈 Price Increased."

            else:
                message = "⚖️ Price Unchanged."

        else:
            message = "ℹ️ First time tracking this product."

        prices[product] = current_price
        save_prices(prices)

    return render_template("index.html", message=message, old_price=old_price)

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)