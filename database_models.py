from app import *
import uuid
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from constants import DATABASE_URL

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    dept = db.Column(db.String(100))
    year = db.Column(db.Integer)
    section = db.Column(db.String(10))
    roll_no = db.Column(db.String(20))
    mode_of_payment = db.Column(db.String(20))
    payment_status = db.Column(db.String(20))
    workshop = db.Column(db.String(100))
    merchant_transaction_id = db.Column(db.String(100))
    day1_attendance = db.Column(db.Boolean, default=False)
    day2_attendance = db.Column(db.Boolean, default=False)
    misc_1_attendance = db.Column(db.Boolean, default=False)  # New column
    misc_2_attendance = db.Column(db.Boolean, default=False)  # New column
    
    @staticmethod
    def generate_unique_transaction_id():
        new_transaction_id = str(uuid.uuid4())
        while Transaction.query.filter_by(merchant_transaction_id=new_transaction_id).first() is not None:
            # If the generated transaction ID already exists, regenerate a new one
            new_transaction_id = str(uuid.uuid4())
        return new_transaction_id




    
with app.app_context():
    db.create_all()
