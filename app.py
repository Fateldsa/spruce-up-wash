from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')  # Your email where bookings will be sent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        service = request.form['service']
        date = request.form['date']
        notes = request.form['notes']
        
        # Create email message
        subject = f"New Booking from {name}"
        body = f"""
        New booking request received:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Address: {address}
        Service: {service}
        Preferred Date: {date}
        Notes: {notes}
        """
        
        try:
            # Send email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = TO_EMAIL
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, text)
            server.quit()
            
            flash('Your booking was successful! We will contact you soon.', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('There was an error processing your booking. Please try again later.', 'error')
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
