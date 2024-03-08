import datetime
import re
import uuid

from flask import Flask, render_template
from flask import request, jsonify, session, redirect, url_for
from flask_session import Session
import firebase_admin
from firebase_admin import credentials, db, storage

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '09120125'
Session(app)
cred = credentials.Certificate("soap-df2ab-firebase-adminsdk-u7cvg-1f48e561a6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://soap-df2ab-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'soap-df2ab.appspot.com'
})

bucket = storage.bucket()
start_order_id = 100

@app.route('/')
def retrieve_menu():

    menu_ref = db.reference("Menu/Food").get()
    menu = sorted(menu_ref.items(), key=lambda x: x[0])
    print(menu)
    blobs = bucket.list_blobs(prefix="Food/")
    urls = []
    # test

    menu = []

    for item_name, item_data in menu_ref.items():

        print(f"Item Name: {item_name}, Item Data: {item_data}")
        # Check if the 'price' field exists in the item's data

        if isinstance(item_data, dict):
            price = item_data.get('Price', 'N/A')
        else:
            price = 'N/A'

        # Add the item's details to the menu list
        menu.append({
            'name': item_name,
            'price': price
        })

    for blob in blobs:
        url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
        urls.append(url)

    return render_template('index.html', menu=menu, urls=urls)


@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json()

    # Update the cart in the session
    item_name = data.get('item')
    print(f"Updating cart for item: {item_name}")

    if 'cart' not in session:
        session['cart'] = {}

    session['cart'][item_name] = session['cart'].get(item_name, 0) + 1
    # Debug print statements
    print(f"Updated cart: {session['cart']}")

    # Return the updated cart count
    return jsonify({'cart_count': session['cart'][item_name], 'item_name': item_name})


@app.route('/cart',)
def view_carts():
    cart_items = session.get('cart', {})
    items = []
    info = []

    for item_name, quantity in cart_items.items():
        item_info = get_database(item_name)
        if item_info:
            items.append({
                'name': item_name,
                'quantity': quantity
            })
            info.append({
                'name': item_name,
                'quantity': quantity,
                'price': item_info['price']
            })
        return render_template('cart.html', items=info)


def get_database(item_name):
    menu_ref = db.reference("Menu/Food").get()

    if isinstance(menu_ref, dict) and item_name in menu_ref:
        item_data = menu_ref[item_name]
        if isinstance(item_data, dict):
            price = item_data.get('Price', 'N/A')
        else:
            price = 'N/A'

        return {
            'name': item_name,
            'price': price
        }
    return {}



@app.route('/Table/NewTable')
def new_Table():
    return 0


@app.route('/Table/ChangeTable')
def change_Table():
    return 0


@app.route('/Orders/PlaceOrder', methods = ['POST'])
def place_Order():
    global start_order_id
    cart_items = session.get('cart', {})

    item_names = list(cart_items.keys())
    order_id = start_order_id
    start_order_id += 1
    order_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:$S')
    order_data = {
        'id': order_id,
        'items': item_names,
        'ordertime': order_time
    }

    orders_ref = db.reference('Orders')
    orders_ref.child(str(order_id)).set(order_data)

    session.pop('cart', None)

    return redirect(url_for('order_Confirmation',order_id = order_id))


@app.route('/Orders/Confirmation/<order_id>')
def order_Confirmation(order_id):
    order_ref = db.reference('Orders').child(order_id)
    order_data = order_ref.get()
    if order_data:
        return render_template('confirmation.html', order = order_data)
    else:
        return render_template('error.html', message = 'Order not found')


@app.route('/Orders/Update')
def order_Update():
    return 0


@app.route('/Orders/Cancel')
def order_Cancel():
    return 0


@app.route('/Payments/MakePayment')
def payment_Make():
    return 0


@app.route('/Payments/CollectPayment')
def payment_Collect():
    return 0


@app.route('/Payments/RetrievePayment')
def payment_Retrieve():
    return 0


@app.route('/Ingredients/IngCheck')
def Ing_Check():
    return 0


if __name__ == '__main__':
    app.run(debug=True)

