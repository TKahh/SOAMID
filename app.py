from flask import Flask

app = Flask(__name__)


@app.route('/menu')
def retrieve_Menu():
    menu = []
    return menu


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


@app.route('/Items/Update')
def Items_Update():
    return 0


if __name__ == '__main__':
    app.run()
