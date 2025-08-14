from flask import Flask, request, jsonify, render_template, redirect, url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
from telegram import Bot
from dotenv import load_dotenv
import os
import requests
#import convertapi

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

# Telegram bot token and chat ID (loaded from .env), defining send-function
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HOST_IP = os.getenv('HOST_IP')
HOST_PORT = os.getenv('HOST_PORT')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("Message sent successfully")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bread = db.Column(db.Integer, nullable=False)
    sweets = db.Column(db.String(3), nullable=False)
    bars = db.Column(db.String(3), nullable=False)
    choco = db.Column(db.String(3), nullable=False)
    fruits = db.Column(db.String(3), nullable=False)
    vegetable = db.Column(db.String(3), nullable=False)
    collegeAvailable = db.Column(db.String(3), nullable=False)
    comments = db.Column(db.String(256))
    timestamp = db.Column(db.String(30), nullable=False)

@app.route('/')
def index():
    return render_template('index.html', title="Schnubbis Frühstück Order", section="Schnubbis frühstück order")

@app.route('/success')
def success():
    # Fetch cat fact
    response = requests.get('https://catfact.ninja/fact')
    cat_fact = response.json().get('fact', 'No cat fact available')

    # Fetch cat picture
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_picture_url = response.json()[0].get('url', '') if response.status_code == 200 else ''

    return render_template('success.html', title="Gesendet :3", cat_picture_url=cat_picture_url, cat_fact=cat_fact)

@app.route('/submit', methods=['POST'])
def submit_order():
    data = {
        'bread': request.form['bread'],
        'sweets': 'Yes' if request.form.get('sweets') else 'No',
        'bars': 'Yes' if request.form.get('bars') else 'No',
        'choco': 'Yes' if request.form.get('choco') else 'No',
        'fruits': 'Yes' if request.form.get('fruits') else 'No',
        'vegetable': 'Yes' if request.form.get('vegetable') else 'No',
        'collegeAvailable': 'Yes' if request.form.get('college-available') else 'No',
        'comments': request.form['comments']
    }
    timestamp = datetime.datetime.now().isoformat()

    # Add timestamp to the data
    data['timestamp'] = timestamp

    # Store the order in the database
    new_order = Order(
        bread=data['bread'],
        sweets=data['sweets'],
        bars=data['bars'],
        choco=data['choco'],
        fruits=data['fruits'],
        vegetable=data['vegetable'],
        collegeAvailable=data['collegeAvailable'],
        comments=data['comments'],
        timestamp=timestamp
    )
    db.session.add(new_order)
    db.session.commit()

    # Send a message via Telegram with the order details
    order_message = (
        f"New Order:\n"
        f"Bread: {data['bread']}\n"
        f"Sweets: {data['sweets']}\n"
        f"Bars: {data['sweets']}\n"
        f"Choco: {data['sweets']}\n"
        f"Fruits: {data['fruits']}\n"
        f"Vegetable: {data['vegetable']}\n"
        f"College Available: {data['collegeAvailable']}\n"
        f"Comments: {data['comments']}\n"
        f"Timestamp: {timestamp}"
    )
    send_telegram_message(order_message)

    # return jsonify({"status": "success", "data": data}), 201
    return redirect(url_for('success'))

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        orders_list.append({
            'id': order.id,
            'bread': order.bread,
            'sweets': order.sweets,
            'bars': order.bars,
            'choco': order.choco,
            'fruits': order.fruits,
            'vegetable': order.vegetable,
            'collegeAvailable': order.collegeAvailable,
            'comments': order.comments,
            'timestamp': order.timestamp
        })
    return jsonify(orders_list), 200


@app.route('/admin')
def admin():
    orders = Order.query.all()
    return render_template('admin.html', orders=orders)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_order(id):
    order = Order.query.get(id)
    if order:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('admin'))

# Custom filter for enumerate
@app.template_filter('enumerate')
def jinja2_enumerate(iterable):
    return enumerate(iterable)

if __name__ == '__main__':
    # Create the database and tables
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=HOST_PORT, host=HOST_IP)