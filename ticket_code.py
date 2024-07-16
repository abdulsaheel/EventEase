from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
from cryptography.fernet import Fernet

# Hardcoded key (it should be a URL-safe base64-encoded 32-byte key)
key = b'wM04I6H-c_mYNZ8Kre7mly_VgbNvvyo3FGnlo-On9cA='
cipher_suite = Fernet(key)

def encrypt_string(plain_text):
    cipher_text = cipher_suite.encrypt(plain_text.encode())
    return cipher_text.decode()


def generate_ticket(transaction_data):
    # Open the image
    image = Image.open("ticket.png")

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Set the font and font size
    font = ImageFont.truetype("ovo-font.ttf", size=30)
    workshop_font = ImageFont.truetype("ovo-font.ttf", size=70)

    # Define the text positions
    name_pos = (1320, 80)
    mobile_pos = (1320, 160)
    email_pos = (1320, 240)
    department_pos = (1320, 320)
    year_pos = (1320, 400)
    section_pos = (1320, 480)
    roll_number_pos = (1320, 560)
    workshop_pos = (700, 530)

    # Write the text on the image using transaction data
    draw.text(name_pos, f"Name: {transaction_data.name}", font=font, fill=(0, 0, 0))
    draw.text(mobile_pos, f"Mobile: {transaction_data.mobile_number}", font=font, fill=(0, 0, 0))
    draw.text(email_pos, f"Email: {transaction_data.email}", font=font, fill=(0, 0, 0))
    draw.text(department_pos, f"Department: {transaction_data.dept}", font=font, fill=(0, 0, 0))
    draw.text(year_pos, f"Year: {transaction_data.year}", font=font, fill=(0, 0, 0))
    draw.text(section_pos, f"Section: {transaction_data.section}", font=font, fill=(0, 0, 0))
    draw.text(roll_number_pos, f"Roll Number: {transaction_data.roll_no}", font=font, fill=(0, 0, 0))
    draw.text(workshop_pos, transaction_data.workshop, font=workshop_font, fill=(0, 0, 0))

    # Generate QR code
    qr_data = encrypt_string(transaction_data.roll_no)  # Replace with your desired data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="transparent")

    # Resize the QR code image to match the desired area
    qr_pos = (880, 120)  # Adjust the position as needed
    qr_size = (400, 400)  # Adjust the size as needed
    qr_img = qr_img.resize(qr_size)

    # Paste the QR code onto the image
    image.alpha_composite(qr_img, dest=qr_pos)

    # Save the modified image to a BytesIO object
    img_io = BytesIO()
    image.save(img_io, format='PNG')
    image.close()
    img_io.seek(0)

    return img_io


