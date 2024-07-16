
---

# EventEase by Digi Vyaapar

![Digi Vyaapar](https://i.ibb.co/n8VZmBc/office-digivyaapar-link.png)

Welcome to **EventEase** by **Digi Vyaapar**! This project exemplifies our commitment to excellence in software development. EventEase is designed to streamline event registration, ticketing, and attendee management with seamless integration of WhatsApp and email notifications. 🎟️📧

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
5. [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [API Endpoints](#api-endpoints)
6. [Screenshots](#screenshots)
7. [Notes for Users](#notes-for-users)
8. [Upcoming App](#upcoming-app)
9. [Contributors](#contributors)
10. [License](#license)
11. [Acknowledgements](#acknowledgements)

## Project Overview

![Project Image](https://i.ibb.co/gWXmDSX/Best-Way-To-Tracking-Your-Event.png)

**EventEase** by **Digi Vyaapar** is crafted to manage event registrations efficiently. It allows users to register for events, receive confirmation emails and WhatsApp messages with QR codes, and ensures smooth check-ins with real-time attendance tracking.

## Key Features

- 🎟️ **Ticketing System**: Efficiently handles registrations and ticket generation.
- 💸 **PhonePe Integration**: Secure and reliable payment processing using PhonePe.
- 📧 **Email Notifications**: Sends confirmation emails with event details and QR codes.
- 📱 **WhatsApp Integration**: Sends WhatsApp messages with QR codes for quick check-ins.
- 📅 **Attendance Tracking**: Real-time tracking of attendee check-ins and workshop participation.
- 🔒 **Secure Data Handling**: Ensures data security with encryption and safe storage practices.

## Technologies Used

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **API Integration**: PhonePe API, WhatsApp API, Gmail SMTP
- **Utilities**: UUID for unique transaction IDs, Cryptography for data encryption

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- PostgreSQL
- Flask and related dependencies
- Access to PhonePe, Gmail SMTP, and WhatsApp API credentials

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/eventease.git
   cd eventease
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the Flask Application**
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`.

### API Endpoints

- **GET /register**: Displays the registration form.
- **POST /register**: Processes registration and triggers email/WhatsApp notifications.
- **POST /check-in**: Processes QR code scans and updates attendance.
- **GET /**: Displays the homepage.
- **GET /success/<encrypted_data>**: Displays the success page with the ticket QR code after successful payment.
- **POST /ticket-response**: Receives ticket responses and updates the payment status.
- **GET, POST /login**: Displays the login form and processes login credentials.
- **GET /logout**: Logs out the current user.
- **GET /admin-panel**: Displays the admin panel with transaction data (login required).
- **POST /update-transaction**: Updates transaction details from the admin panel.
- **GET /send_mail/<merchant_transaction_id>**: Sends an email with the transaction details.
- **GET, POST /add_offline_registrant**: Adds offline registrants to the system.
- **POST /mark_attendance**: Marks attendance for the given roll number and attendance type.

## Screenshots

### Confirmation Email
![Confirmation Email](https://i.ibb.co/4mf909k/Automated-Mails.png)

### WhatsApp Notification
![WhatsApp Notification](https://i.ibb.co/yQW9n5s/Untitled-design.png)

## Notes for Users

We kept this code in a kind of unedited state that actually contains event details so that you can easily understand the features and edit them for your own use.

## Upcoming App

We have also developed an app that follows this schema, which will be released later. Stay tuned for updates! For more information, visit [Digi Vyaapar](https://digivyaapar.link).

## Unofficial Whatsapp API

In this project, we have used the Unofficial WhatsApp API. For more information, visit [go-whatsapp-web-multidevice](https://github.com/aldinokemal/go-whatsapp-web-multidevice) and for code-related API Implementation, visit this [Unofficial WhatsApp API](https://github.com/abdulsaheel/).

## Disclaimer

**EventEase** by **Digi Vyaapar** is provided as-is without any warranties or guarantees. We do not hold any responsibility for any repercussions arising from the use of this code.

## For Similar Projects

For similar secure and long-term projects, please visit us at [Digi Vyaapar](https://digivyaapar.link). We specialize in building scalable software solutions tailored to meet your business needs.

## Contributors

- [Abdul Sahil](https://github.com/abdulsaheel)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PhonePe API](https://www.phonepe.com/developer)
- [Gmail SMTP](https://support.google.com/mail/answer/7126229)
- [Unofficial WhatsApp API](https://github.com/aldinokemal/go-whatsapp-web-multidevice)

---

Feel free to reach out with any questions or feedback. Happy coding! 🎉

---

