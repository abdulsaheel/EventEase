from mail_code import *
from functools import wraps
from ticket_code import *
from app import *
from database_models import *
from phonepe_utils import *
from utils import *
from constants import *



@app.route('/register', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        dept = request.form['dept']
        year = request.form['year']
        section = request.form['section']
        roll_no = request.form['roll_no']
        workshop = request.form['workshop']
        transaction_id = Transaction.generate_unique_transaction_id()
        encrypted_data=encrypt_string(roll_no)
        redirect_url=f"{base_redirect_url}/{encrypted_data}"

        phonepe = create_phonepe_instance(merchant_id=merchant_id, phone_pe_salt=salt_key, phone_pe_host=host_url, redirect_url=redirect_url, webhook_url=webhook_url)
        # Check if the roll_no already exists and the status is SUCCESS
        existing_transaction = Transaction.query.filter_by(roll_no=roll_no).first()
        if existing_transaction:
            # Check if the existing transaction's payment status is SUCCESS
            if existing_transaction.payment_status == 'SUCCESS':
                error_message = f"Roll number {roll_no} already exists. If you think this is a mistake, please contact us at your earliest convenience."
                return render_template('payment_form.html', error_message=error_message)


        # Create transaction with PhonePe
        order_data = phonepe.create_txn(order_id=transaction_id, amount=24900, user=roll_no)
        
        # Create a new transaction row
        new_transaction = Transaction(
            name=name,
            mobile_number=mobile_number,
            email=email,
            dept=dept,
            year=year,
            section=section,
            roll_no=roll_no,
            workshop=workshop,
            merchant_transaction_id=transaction_id,
            mode_of_payment='online',
            payment_status='initiated'
        )
        
        # Add and commit transaction to database
        db.session.add(new_transaction)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            error_message = "Roll number already exists"
            return render_template('payment_form.html', error_message=error_message)

        # Extract Payment Link
        link = order_data["data"]["instrumentResponse"]["redirectInfo"]["url"]

        # Redirect user to payment link
        return redirect(link)
    else:
        # Render form template for user input
        return render_template('payment_form.html')

@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('index.html')


@app.route('/success/<encrypted_data>', methods=['GET', 'POST'])
def ticket(encrypted_data):
    try:
        # Decrypt the data
        roll_no = decrypt_string(encrypted_data)
    except Exception as e:
        print(f"Decryption error: {e}")
        return render_template('failure.html')

    # Query the transaction from the database
    transaction = Transaction.query.filter_by(roll_no=roll_no, payment_status='SUCCESS').first()

    # If no transaction found or payment not successful
    if not transaction:
        return render_template('failure.html')

    # Generate the QR code URL
    qr_code_url = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={encrypted_data}'
    
    # Render the success template with the transaction and QR code URL
    return render_template('payment_success.html', transaction=transaction, qr_code_url=qr_code_url)


@app.route('/ticket-response', methods=['POST'])
def ticket_response():
    encode_data = request.json
    data= decode_base64(encode_data['response'])
    print(data)
    if data.get('success') and data.get('code') == 'PAYMENT_SUCCESS':

        merchant_transaction_id = data['data']['merchantTransactionId']
        print(merchant_transaction_id)
        # Update payment status to 'SUCCESS' based on merchant transaction ID
        transaction = Transaction.query.filter_by(merchant_transaction_id=merchant_transaction_id).first()
        if transaction:
            transaction.payment_status = 'SUCCESS'
            db.session.commit()
            qr_data=encrypt_string(transaction.roll_no)
            send_message_and_email(transaction,qr_data)

    return "Ticket response received successfully!"



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login.html', error_message='Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))

# Decorator to check if the user is logged in before accessing admin panel
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Flask route for admin panel
@app.route('/admin-panel')
@login_required
def admin_panel():
    # Retrieve data from the database
    transactions = Transaction.query.all()
    
    # Prepare data for Handsontable
    data = [
        [transaction.id, transaction.name, transaction.mobile_number, transaction.email, transaction.dept, transaction.year, transaction.section, transaction.roll_no, transaction.mode_of_payment, transaction.payment_status, transaction.workshop, transaction.merchant_transaction_id] 
        for transaction in transactions
    ]
    
    # Pass data to the template
    return render_template('admin_panel.html', data=data)

@app.route('/update-transaction', methods=['POST'])
def update_transaction():
    updated_data = request.get_json()

    # Update the database with the new data
    for updated_row in updated_data:
        transaction_id = updated_row[0]  # Assuming ID is the first column
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            # Update transaction attributes
            transaction.name = updated_row[1]
            transaction.mobile_number = updated_row[2]
            transaction.email = updated_row[3]
            transaction.dept = updated_row[4]
            transaction.year = updated_row[5]
            transaction.section = updated_row[6]
            transaction.roll_no = updated_row[7]
            transaction.mode_of_payment = updated_row[8]
            transaction.payment_status = updated_row[9]
            transaction.workshop = updated_row[10]
            transaction.merchant_transaction_id = updated_row[11]

            db.session.commit()

    return jsonify({'success': True})

@app.route('/send_mail/<merchant_transaction_id>', methods=['GET'])
def send_mail(merchant_transaction_id):
    # Retrieve transaction details from the database based on the merchant_transaction_id
    transaction = Transaction.query.filter_by(merchant_transaction_id=merchant_transaction_id).first()

    if transaction.payment_status=='SUCCESS':

        qr_data=encrypt_string(transaction.roll_no,)
        send_message_and_email(transaction,qr_data)
        # You can add code here to send an email using the retrieved transaction details
        return jsonify({'success': True, 'message': 'Mail sent successfully.'})
    elif transaction.payment_status=='SUCCESS':
        return jsonify({'success': False, 'message': 'Payment Not Successful.'})
    else:
        return jsonify({'success': False, 'message': 'Transaction not found.'})
    


@app.route('/add_offline_registrant', methods=['GET','POST'])
def add_offline_regsitrant():
    if request.method == 'GET':
        return render_template('add_offline_registrant.html')
    
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        mobile_number = data.get('mobile_number')
        email = data.get('email')
        dept = data.get('dept')
        year = data.get('year')
        section = data.get('section')
        roll_no = data.get('roll_no')
        mode_of_payment = data.get('mode_of_payment')
        workshop = data.get('workshop')
        print(data)
        # Check if the roll number already exists
        existing_transaction = Transaction.query.filter_by(roll_no=roll_no,payment_status='SUCCESS').first()

        if existing_transaction:
            return jsonify({'message': 'Roll number already present'}), 400
        transaction_id=Transaction.generate_unique_transaction_id()
        # Create a new transaction
        new_transaction = Transaction(
            name=name,
            mobile_number=mobile_number,
            email=email,
            dept=dept,
            year=year,
            section=section,
            roll_no=roll_no,
            merchant_transaction_id=transaction_id,
            mode_of_payment=mode_of_payment,
            payment_status='SUCCESS',
            workshop=workshop
        )
        db.session.add(new_transaction)
        db.session.commit()
        qr_data=encrypt_string(roll_no)
        send_message_and_email(new_transaction,qr_data)

        return redirect(url_for('admin_panel'))
    
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    roll_no = data.get('roll_no')
    attendance_type = data.get('attendance_type')
    print("Roll Number: ", roll_no)
    print("Attendance Type: ", attendance_type)
    if not roll_no or not attendance_type:
        return jsonify({'status': 'error', 'message': 'Missing roll_no or attendance_type'}), 400

    attendance_column = None
    if attendance_type == 'day_1':
        attendance_column = 'day1_attendance'
    elif attendance_type == 'day_2':
        attendance_column = 'day2_attendance'
    elif attendance_type == 'misc_1':
        attendance_column = 'misc_1_attendance'
    elif attendance_type == 'misc_2':
        attendance_column = 'misc_2_attendance'
    else:
        return jsonify({'status': 'error', 'message': 'Invalid attendance_type'}), 400

    transaction = Transaction.query.filter_by(roll_no=roll_no, payment_status='SUCCESS').first()
    if not transaction:
        return jsonify({'status': 'not_found', 'message': 'Transaction not found for the provided roll_no or payment_status is not SUCCESS'}), 404

    if getattr(transaction, attendance_column):
        return jsonify({'status': 'already_marked', 'message': f'{attendance_type} is already marked as present for roll number {roll_no}'}), 200

    print(transaction)
    setattr(transaction, attendance_column, True)
    db.session.commit()
    send_whatsapp_message(transaction.mobile_number, message = f"  {attendance_type.capitalize()} marked as present for roll number {roll_no}. We hope you gained valuable insights from our workshop and look forward to seeing you at future sessions!")
    return jsonify({'status': 'marked', 'message': f'{attendance_type} marked as present for roll number {roll_no}'}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6969)
