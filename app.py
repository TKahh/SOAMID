from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

orders = []

@app.route('/place_order', methods=['POST'])
def place_order():
    order_info = request.json
    orders.append(order_info)
    return jsonify({'message': 'Order placed successfully'})

@app.route('/check_order', methods=['GET'])
def check_order():
    phone_number = request.args.get('phone_number')
    table_number = request.args.get('table_number')
    for order in orders:
        if order['phone_number'] == phone_number and order['table_number'] == table_number:
            return jsonify(order)
    return jsonify({'message': 'Order not found'})

@app.route('/edit_order', methods=['PUT'])
def edit_order():
    order_info = request.json
    phone_number = order_info['phone_number']
    table_number = order_info['table_number']
    for order in orders:
        if order['phone_number'] == phone_number and order['table_number'] == table_number:
            order['food'] = order_info['food']
            order['quantity'] = order_info['quantity']
            order['note'] = order_info['note']
            return jsonify({'message': 'Order edited successfully'})
    return jsonify({'message': 'Order not found'})

@app.route('/cancel_order', methods=['DELETE'])
def cancel_order():
    phone_number = request.args.get('phone_number')
    table_number = request.args.get('table_number')
    for order in orders:
        if order['phone_number'] == phone_number and order['table_number'] == table_number:
            orders.remove(order)
            return jsonify({'message': 'Order canceled successfully'})
    return jsonify({'message': 'Order not found'})

@app.route('/send_notification', methods=['POST'])
def send_notification():
    notification_info = request.json
    # Code to send notification to specified recipients
    return jsonify({'message': 'Notification sent successfully'})

@app.route('/manage_food', methods=['PUT'])
def manage_food():
    food_info = request.json
    # Code to manage food (e.g., update food status)
    return jsonify({'message': 'Food managed successfully'})


@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run()