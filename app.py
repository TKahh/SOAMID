import datetime
import re
from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db, storage

app = Flask(__name__, static_folder='static')
cred = credentials.Certificate("D:/SOAMID/soap-df2ab-firebase-adminsdk-u7cvg-1f48e561a6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://soap-df2ab-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'soap-df2ab.appspot.com'
})

bucket = storage.bucket()


@app.route('/')
def retrieve_Menu():
    menu_top3_ref = db.reference("Menu/Food")
    menu_top3_snapshot = menu_top3_ref.order_by_key().limit_to_first(3).get()
    menu_top3 = []
    for key, value in menu_top3_snapshot.items():
        item = {
            'key': key,
            'name': value.get('name', ''),
            'image_url': value.get('image_url', '')
        }
        menu_top3.append(item)

    urls = [get_image_url(item, bucket) for item in menu_top3]
    print(urls)
    return render_template('index.html', menu_top3=menu_top3, urls=urls)


def get_image_url(menu_item, bucket):
    image_url = menu_item.get('image_url', '')
    if not image_url or not re.match(r'^[a-zA-Z0-9_]+$', image_url):
        return None  # Trả về url mặc định hoặc xử lý error khác

    blob_name = f"Food/{image_url}"

    if bucket.blob_exists(blob_name):
        blob = bucket.get_blob(blob_name)
        print(f"Thành công: {blob_name}")
        return blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    else:
        print(f"not found: {blob_name}")
        return None  # Trả về url mặc định hoặc xử lý error khác

print(get_image_url({'image_url': 'food-1.jpg'}, bucket))






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
