from bs4 import BeautifulSoup
import re
import json
import os
import smtplib
from email.mime.text import MIMEText

# ===============================
# CLEAN PRICE FUNCTION
# ===============================
def clean_price(price):
    numbers = re.findall(r'\d+', price)
    return int("".join(numbers))

# ===============================
# LOAD PREVIOUS PRICES
# ===============================
def load_prices():
    if os.path.exists("prices.json"):
        with open("prices.json", "r") as file:
            return json.load(file)
    return {}

# ===============================
# SAVE PRICES
# ===============================
def save_prices(data):
    with open("prices.json", "w") as file:
        json.dump(data, file)

# ===============================
# SEND EMAIL FUNCTION
# ===============================
def send_email(product, old_price, new_price):
    try:
        print("📧 Attempting to send email...")

        sender = "vadlapudisrinivas30@gmail.com"  # MUST match app password account
        receiver = "bsujithbsujith53@gmail.com"  # Can be same or different
        password = "ptabokjrtecoqigj"  # Remove spaces

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

        print("✅ Email Sent Successfully!")

    except Exception as e:
        print("❌ Email Error:", e)

# ===============================
# MAIN RUNTIME INITIALIZATION
# ===============================
def main():
    print("🚀 Starting Price Tracker...\n")

    # Open product file
    with open("laptop.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    price_tag = soup.find("span", {"class": "price"})

    if not price_tag:
        print("❌ Price tag not found!")
        return

    current_price = clean_price(price_tag.text)
    print("Current Price:", current_price)

    prices = load_prices()
    product_name = "Laptop"

    if product_name in prices:
        old_price = prices[product_name]
        print("Old Price:", old_price)

        if current_price < old_price:
            print("🔥 Price Dropped!")
            send_email(product_name, old_price, current_price)

        elif current_price > old_price:
            print("📈 Price Increased.")

        else:
            print("⚖️ Price Unchanged.")

    else:
        print("ℹ️ First time tracking this product.")

    prices[product_name] = current_price
    save_prices(prices)

    print("\n✅ Price stored successfully.")
    print("🏁 Program Finished.")

# ===============================
# RUN PROGRAM
# ===============================
if __name__ == "__main__":
    main()