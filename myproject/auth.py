import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from flask import session

# Dictionary to store OTPs and their expiration times
otp_store = {}

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp):
    """Send OTP to user's email"""
    # Email configuration - should be moved to environment variables in production
    sender_email = os.environ.get('EMAIL_USER', 'your-email@example.com')
    sender_password = os.environ.get('EMAIL_PASSWORD', 'your-email-password')
    
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Your One-Time Password for Diet Planner'
    
    # Email body
    body = f"""
    <html>
    <body>
        <h2>Your One-Time Password</h2>
        <p>Hello,</p>
        <p>Your OTP for authentication is: <strong>{otp}</strong></p>
        <p>This OTP will expire in 10 minutes.</p>
        <p>If you did not request this OTP, please ignore this email.</p>
        <p>Thank you,<br>Diet Planner Team</p>
    </body>
    </html>
    """
    
    message.attach(MIMEText(body, 'html'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def store_otp(email, otp, expiry_minutes=10):
    """Store OTP with expiration time"""
    expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
    otp_store[email] = {
        'otp': otp,
        'expiry': expiry_time
    }

def verify_otp(email, user_otp):
    """Verify the OTP entered by user"""
    if email not in otp_store:
        return False
    
    stored_data = otp_store[email]
    
    # Check if OTP has expired
    if datetime.now() > stored_data['expiry']:
        del otp_store[email]
        return False
    
    # Check if OTP matches
    if stored_data['otp'] == user_otp:
        # OTP verified, remove it from store
        del otp_store[email]
        return True
    
    return False

def send_and_store_otp(email):
    """Generate, send and store OTP"""
    otp = generate_otp()
    if send_otp_email(email, otp):
        store_otp(email, otp)
        return True
    return False

def is_authenticated():
    """Check if user is authenticated"""
    return session.get('user_authenticated', False)

def set_authenticated(status=True):
    """Set authentication status in session"""
    session['user_authenticated'] = status