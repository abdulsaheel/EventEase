from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from io import BytesIO
import emoji
import requests
from email.utils import formataddr
import emoji
from constants import SENDER_EMAIL, APP_SPECIFIC_PASSWORD


def send_message(Transaction,qr_data):
    image_url=f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}'
    
    # Download the image
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    
    url = "https://YOUR_WHATSAPP_API_DEPLOYED_IP:PORT/send/image"

    # Custom message with emojis
    custom_message =  f"""
Hi {{name}} {emoji.emojize(':wave:',language='alias')},

{emoji.emojize(':tada:', language='alias')}  *Congratulations!* {emoji.emojize(':tada:', language='alias')} 

You have successfully registered for the *PRAESTO 2K24* - Annual Event organized by the *Atharva Data Science Community* at Malla Reddy Engineering College.

{emoji.emojize(':clipboard:')} *Here are your registration details:*

    - *Mobile Number:* {{mobile_number}}
    - *Email:* {{email}}
    - *Department:* {{dept}}
    - *Year:* {{year}}
    - *Section:* {{section}}
    - *Roll Number:* {{roll_no}}
    - *Workshop:* {{workshop}}
{emoji.emojize(':rocket:')} To make your check-in process smoother, please present the following *QR code* at the event entrance. This QR code serves as your ticket {emoji.emojize(':ticket:')}.

We're excited to have you join us for a series of insightful workshops, and other tech-related activities {emoji.emojize(':robot:')}{emoji.emojize(':books:')}.

Stay tuned for more updates and detailed event schedules {emoji.emojize(':calendar:')}. If you have any questions, feel free to contact us at {emoji.emojize(':telephone_receiver:')} 8074914825(Nithish - President), 9912810374(Bhavani Prasad - Vice President), or 8688621370(Abdul Sahil - Vice President).

Best regards,  
*Atharva Data Science Community*  
Malla Reddy Engineering College (A)
"""


    formatted_message = custom_message.format(name=Transaction.name, mobile_number=Transaction.mobile_number, email=Transaction.email, dept=Transaction.dept, year=Transaction.year, section=Transaction.section, roll_no=Transaction.roll_no, workshop=Transaction.workshop)
    

    # Now use this encoded message in your payload
    payload = {
        'phone': f'91{Transaction.mobile_number}@s.whatsapp.net',
        'caption': formatted_message,
        'view_once': 'false',
        'compress': 'false'
    }

    
    files = {
        'image': ('image.jpg', image_data, 'image/jpeg')
    }

    headers = {
        'Content-Type': 'multipart/form-data'
    }

    response = requests.post(url, data=payload, files=files)
    response_json = response.json()
    print(response_json)
    if response_json.get("code") == "SUCCESS":
        print("Message Sent Succesfully")
        return True
    else:
        print("Error sending message:", response_json.get("message"))
        return False

def send_email_with_qr_code(transaction, qr_data):
    # Gmail SMTP server details
    smtp_server = 'smtp.gmail.com'
    port = 587  # For starttls
    sender_email = SENDER_EMAIL  # Enter your address
    password = APP_SPECIFIC_PASSWORD

    # Create a multipart message and set headers
    message = MIMEMultipart()
    
    # Custom name for the sender
    sender_name = 'PRAESTO 2K24 Ticket - ADSC'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = formataddr((sender_name, sender_email))
    message['To'] = transaction.email
    message['Subject'] = 'Registration Confirmation for PRAESTO Event'

    # HTML body of the email with dynamically generated QR code
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="text-align: center; margin-top: 20px;">
            <img src="https://i.ibb.co/MGDMbmL/praesto-2k24-logo-1.png" alt="PRAESTO Logo" style="max-width: 200px;">
        </div>
        <div style="background-color: #FFDAB9; padding: 20px; border-radius: 10px; margin-top: 20px;">
            <h2 style="color: #FF4500;">Registration Confirmation</h2>
            <p>Dear {transaction.name},</p>
            <p>Thank you for registering for the PRAESTO 2K24. Your registration details are as follows:</p>
            <ul style="list-style-type: none; padding: 0;">
                <li><strong>Name:</strong> {transaction.name}</li>
                <li><strong>Mobile Number:</strong> <a href="tel:{transaction.mobile_number}">{transaction.mobile_number}</a></li>
                <li><strong>Email:</strong> {transaction.email}</li>
                <li><strong>Department:</strong> {transaction.dept}</li>
                <li><strong>Year:</strong> {transaction.year}</li>
                <li><strong>Section:</strong> {transaction.section}</li>
                <li><strong>Roll No:</strong> {transaction.roll_no}</li>
                <li><strong>Workshop Enrolled For:</strong> {transaction.workshop}</li>
            </ul>
            <p>If you find any mistake in the details above, kindly contact us immediately at :</p>
            <ul style="list-style-type: none; padding: 0;">
                <li><a href="tel:+918074914825">8074914825</a></li>
                <li><a href="tel:+9199128103747">9912810374</a></li>
                <li><a href="tel:+918688621370">8688621370</a></li>
            </ul>
            <p>We look forward to seeing you at the event!</p>
            <div style="text-align: center; margin-top: 20px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}" alt="QR Code">
            </div>
        </div>
    </body>
    </html>
    """

    # Attach the HTML body to the email
    message.attach(MIMEText(html, 'html'))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        # Log in to the SMTP server
        server.login(sender_email, password)
        # Send email
        server.sendmail(sender_email, transaction.email, message.as_string())

    print("Email sent successfully!")


def send_whatsapp_message(number,message):
    url = 'https://api.atharvadsc.in/send/message'
    data = {
        'phone': f'91{number}@s.whatsapp.net',
        'message': message,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raise error for non-2xx responses

        if 200 <= response.status_code < 300:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


def send_message_and_email(transaction, qr_data):
    # Call send_message
    message_sent = send_message(transaction,qr_data)
    
    # Call send_email_with_qr_code
    email_sent = send_email_with_qr_code(transaction, qr_data)
    
    # Return True only if both methods are successful
    if message_sent and email_sent:
        return True
    else:
        return False
