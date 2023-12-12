from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db, storage

app = Flask(__name__)
cred = credentials.Certificate("soap-df2ab-firebase-adminsdk-u7cvg-1f48e561a6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://soap-df2ab-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'gs://soap-df2ab.appspot.com'
})
bucket = storage.bucket()


@app.route('/')
def DisplayImage():
    blob = bucket.blob('Food/cutoiyen.jpg')
    image_url = blob.generate_signed_url(expiration=3600)
    return render_template('index.html', image_url=image_url)


@app.route('/menu')
def retrieve_Menu():
    menu = db.reference('Menu').get()
    return str(menu)


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
    app.run()