import datetime
import re
from flask import Flask, render_template
from flask import request, jsonify, session
from flask_session import Session
import firebase_admin
from firebase_admin import credentials, db, storage

app = Flask(__name__, static_folder='static')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '09120125'
Session(app)
cred = credentials.Certificate("soap-df2ab-firebase-adminsdk-u7cvg-1f48e561a6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://soap-df2ab-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'soap-df2ab.appspot.com'
})

bucket = storage.bucket()


@app.route('/')
def retrieve_menu():

    menu_ref = db.reference("Menu/Food").get(shallow=True)
    menu = sorted(menu_ref.items(), key=lambda x: x[0])
    print(menu)
    blobs = bucket.list_blobs(prefix="Food/")
    urls = []
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
    return jsonify({'cart_count': session['cart'][item_name]})


@app.route('/Table/NewTable')
def new_Table():
    return 0


@app.route('/Table/ChangeTable')
def change_Table():
    return 0


@app.route('/Orders/PlaceOrder')
def place_Order():
    return 0


@app.route('/Orders/Confirmation')
def order_Confirmation():
    return 0


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

