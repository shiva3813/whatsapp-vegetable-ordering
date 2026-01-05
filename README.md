# WhatsApp Vegetable & Fruit Ordering System

This project is a WhatsApp-based ordering system that allows users to browse and order vegetables and fruits using a chatbot powered by the Twilio WhatsApp API. Due to WhatsApp interface limitations, product selection with images is implemented through a web-based catalog.

## Features
- WhatsApp chatbot for order interaction
- Image-based product catalog (web)
- Quantity-based ordering
- SQLite database for order storage
- Admin dashboard with order analytics
- Order status management (Confirmed / Delivered)
- Automated WhatsApp delivery notifications

## Technologies Used
- Python (Flask)
- Twilio WhatsApp API
- SQLite
- HTML & CSS

## Environment Variables
Before running the project, set the following environment variables:

TWILIO_ACCOUNT_SID=your_account_sid  
TWILIO_AUTH_TOKEN=your_auth_token  

Note: Actual credentials are not included in this repository for security reasons.

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run: `python app.py`
