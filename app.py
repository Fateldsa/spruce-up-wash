from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from datetime import datetime
import uuid
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-spruce-up-wash-2024'

# Email configuration - Using your SMTP server
SMTP_SERVER = 'box.poorpotato.fun'
SMTP_PORT = 587
EMAIL_ADDRESS = 'mail@swiftvendor.store'
EMAIL_PASSWORD = '123aaa123'
BUSINESS_EMAIL = 'spruceupwash@gmail.com'

# File to store reviews and service IDs
REVIEWS_FILE = 'reviews.json'
SERVICE_IDS_FILE = 'service_ids.json'

def load_reviews():
    try:
        with open(REVIEWS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_review(review):
    reviews = load_reviews()
    reviews.append(review)
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(reviews, f, indent=2)

def load_service_ids():
    try:
        with open(SERVICE_IDS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_service_id(email, service_id, name=""):
    service_ids = load_service_ids()
    if email not in service_ids:
        service_ids[email] = {
            'service_id': service_id,
            'name': name,
            'created_at': datetime.now().isoformat()
        }
        with open(SERVICE_IDS_FILE, 'w') as f:
            json.dump(service_ids, f, indent=2)

def get_or_create_service_id(email, name=""):
    service_ids = load_service_ids()
    if email in service_ids:
        return service_ids[email]['service_id']
    else:
        # Generate new service ID with Halloween theme
        halloween_prefixes = ['SPOOKY', 'HAUNT', 'WITCH', 'GHOST', 'PUMPKIN', 'BAT', 'CAT']
        prefix = random.choice(halloween_prefixes)
        new_service_id = f"{prefix}-{str(uuid.uuid4())[:6].upper()}"
        save_service_id(email, new_service_id, name)
        return new_service_id

def send_halloween_email(to_email, subject, html_content, is_customer=False):
    """Send email using your SMTP server with Halloween theme"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Spruce Up Wash 🎃 <{EMAIL_ADDRESS}>'
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add HTML content
        msg.attach(MIMEText(html_content, 'html'))

        # Connect to SMTP server and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

def create_review_response_email(name, email, rating, service_id, review_text):
    """Create appropriate email response based on rating"""
    
    if rating in [4, 5]:
        subject = "🎃 Thank You for Your Spooktacular Review!"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(135deg, #1a0f0f, #2a1818);
                    color: #ffffff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: #2a1818;
                    border: 3px solid #ff6b00;
                    border-radius: 15px;
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(90deg, #ff6b00, #8b008b);
                    padding: 30px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px;
                }}
                .pumpkin {{
                    font-size: 48px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .service-id {{
                    background: #1a0f0f;
                    border-left: 4px solid #ff6b00;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 5px;
                    font-family: monospace;
                }}
                .footer {{
                    background: #1a0f0f;
                    padding: 20px;
                    text-align: center;
                    font-size: 14px;
                }}
                .stars {{
                    color: #ff8c00;
                    font-size: 24px;
                    text-align: center;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎃 Thank You for Your Spooktacular Review! 🎃</h1>
                </div>
                <div class="content">
                    <div class="pumpkin">👻</div>
                    <div class="stars">{'★' * rating + '☆' * (5-rating)}</div>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you so much for your {rating}-star review! We're absolutely thrilled that you had a fantastic experience with Spruce Up Wash.</p>
                    <p>Your feedback means the world to us and helps other customers in Fresno discover our professional pressure washing services.</p>
                    <p><strong>Your original review:</strong> "{review_text}"</p>
                    <div class="service-id">
                        <strong>Service ID:</strong> {service_id}
                    </div>
                    <p>We look forward to making your property spooktacular again soon!</p>
                    <p><strong>Need us?</strong> Call (559) 569-5128 or email spruceupwash@gmail.com</p>
                </div>
                <div class="footer">
                    <p>Spruce Up Wash | Fresno, California | Professional Pressure Washing Services</p>
                    <p>© 2023 Spruce Up Wash. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    elif rating == 3:
        subject = "👻 Thanks for Your Feedback"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #1a0f0f; color: #ffffff; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 20px auto; background: #2a1818; border: 3px solid #ff6b00; border-radius: 15px; overflow: hidden; }}
                .header {{ background: linear-gradient(90deg, #ff6b00, #8b008b); padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .service-id {{ background: #1a0f0f; border-left: 4px solid #ff6b00; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .stars {{ color: #ff8c00; font-size: 24px; text-align: center; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h1>👻 Thanks for Your Review 👻</h1></div>
                <div class="content">
                    <div class="stars">{'★' * rating + '☆' * (5-rating)}</div>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you for your {rating}-star review and for choosing Spruce Up Wash.</p>
                    <p>We hope your next experience with us will be even better and fully meet your expectations.</p>
                    <p><strong>Your feedback:</strong> "{review_text}"</p>
                    <div class="service-id"><strong>Service ID:</strong> {service_id}</div>
                    <p>We're always working to improve our services for customers like you.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    else:  # Rating 1-2
        subject = "🕷️ We're Sorry to Hear About Your Experience"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #1a0f0f; color: #ffffff; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 20px auto; background: #2a1818; border: 3px solid #8b008b; border-radius: 15px; overflow: hidden; }}
                .header {{ background: linear-gradient(90deg, #8b008b, #ff6b00); padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .service-id {{ background: #1a0f0f; border-left: 4px solid #8b008b; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .btn {{ background: #ff6b00; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; }}
                .stars {{ color: #ff8c00; font-size: 24px; text-align: center; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h1>🕷️ We're Sorry to Hear About Your Experience 🕷️</h1></div>
                <div class="content">
                    <div class="stars">{'★' * rating + '☆' * (5-rating)}</div>
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you for your honest {rating}-star review. We're genuinely sorry that your experience didn't meet your expectations.</p>
                    <p>We take all feedback seriously and would appreciate if you could share more details about how we can improve.</p>
                    <p><strong>Your comments:</strong> "{review_text}"</p>
                    <div class="service-id"><strong>Service ID:</strong> {service_id}</div>
                    <p><a href="http://localhost:5000/feedback?service_id={service_id}" class="btn">Provide Additional Feedback</a></p>
                    <p>Your input helps us serve you and other customers better in the future.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    return subject, html_content

@app.route('/')
def index():
    reviews = load_reviews()
    # Show last 6 reviews in reverse order (newest first)
    display_reviews = reviews[-6:][::-1] if reviews else []
    return render_template('index.html', reviews=display_reviews)

@app.route('/reviews')
def reviews_page():
    return render_template('review.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        rating = int(request.json.get('rating'))
        text = request.json.get('text')
        
        if not all([name, email, rating, text]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Generate or retrieve service ID
        service_id = get_or_create_service_id(email, name)
        
        review_data = {
            'id': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'rating': rating,
            'text': text,
            'service_id': service_id,
            'date': datetime.now().isoformat(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save review
        save_review(review_data)
        
        # Send appropriate email based on rating
        subject, html_content = create_review_response_email(name, email, rating, service_id, text)
        email_sent = send_halloween_email(email, subject, html_content, True)
        
        # Also send notification to business
        business_subject = f"New {rating}-Star Review from {name}"
        business_html = f"""
        <html>
        <body style="background: #1a0f0f; color: white; padding: 20px;">
            <h2>New Review Received!</h2>
            <p><strong>Customer:</strong> {name} ({email})</p>
            <p><strong>Rating:</strong> {rating}/5 stars</p>
            <p><strong>Service ID:</strong> {service_id}</p>
            <p><strong>Review:</strong> {text}</p>
            <p><strong>Date:</strong> {review_data['timestamp']}</p>
        </body>
        </html>
        """
        send_halloween_email(BUSINESS_EMAIL, business_subject, business_html)
        
        if email_sent:
            return jsonify({'success': True, 'message': 'Review submitted successfully! Thank you email sent.'})
        else:
            return jsonify({'success': True, 'message': 'Review submitted but email failed to send.'})
            
    except Exception as e:
        print(f"Error submitting review: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while submitting your review.'})

@app.route('/booking', methods=['POST'])
def booking():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        service = request.form.get('service')
        date = request.form.get('date')
        notes = request.form.get('notes', '')
        
        # Generate service ID for booking
        service_id = get_or_create_service_id(email, name)
        
        # Create email content for business
        business_email_body = f"""
        <html>
        <body style="background: #1a0f0f; color: white; padding: 20px;">
            <h2>🎃 New Booking Request Received! 🎃</h2>
            <div style="background: #2a1818; padding: 20px; border-radius: 10px;">
                <p><strong>Customer Details:</strong></p>
                <ul>
                    <li><strong>Name:</strong> {name}</li>
                    <li><strong>Email:</strong> {email}</li>
                    <li><strong>Phone:</strong> {phone}</li>
                    <li><strong>Address:</strong> {address}</li>
                    <li><strong>Service:</strong> {service}</li>
                    <li><strong>Preferred Date:</strong> {date}</li>
                    <li><strong>Service ID:</strong> {service_id}</li>
                    <li><strong>Notes:</strong> {notes if notes else 'None'}</li>
                </ul>
                <p><em>Booking received on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            </div>
        </body>
        </html>
        """
        
        # Send email to business
        business_sent = send_halloween_email(BUSINESS_EMAIL, "New Booking Request", business_email_body)
        
        # Send confirmation email to customer
        customer_subject = "🎃 Spruce Up Wash - Booking Confirmation 🎃"
        customer_html = f"""
        <html>
        <body style="background: #1a0f0f; color: white; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #2a1818; border-radius: 15px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #ff6b00, #8b008b); padding: 30px; text-align: center;">
                    <h1>Booking Confirmed! 👻</h1>
                </div>
                <div style="padding: 30px;">
                    <p>Hi <strong>{name}</strong>,</p>
                    <p>Thank you for booking with Spruce Up Wash! We've received your request and will contact you within <strong>24 hours</strong> to confirm your appointment.</p>
                    
                    <div style="background: #1a0f0f; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Service:</strong> {service}</p>
                        <p><strong>Preferred Date:</strong> {date}</p>
                        <p><strong>Service ID:</strong> {service_id}</p>
                    </div>
                    
                    <p>If we're particularly busy on your preferred date, we'll work with you to find the perfect time that works for both of us!</p>
                    
                    <p><strong>Need immediate assistance?</strong> Call us at (559) 569-5128</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        customer_sent = send_halloween_email(email, customer_subject, customer_html, True)
        
        if business_sent and customer_sent:
            flash('Your booking was successful! We will contact you within 24 hours.', 'success')
        else:
            flash('Booking received! There was an issue sending confirmation emails. Please call us at (559) 569-5128 to confirm.', 'warning')
        
        return redirect(url_for('booking_success'))
        
    except Exception as e:
        print(f"Error processing booking: {e}")
        flash('There was an error processing your booking. Please try again or call us at (559) 569-5128.', 'error')
        return redirect(url_for('booking_success'))

@app.route('/booking-success')
def booking_success():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Booking Confirmation - Spruce Up Wash</title>
        <style>
            body { font-family: Arial, sans-serif; background: #1a0f0f; color: white; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .success-card { background: #2a1818; padding: 50px; border-radius: 15px; text-align: center; border: 3px solid #ff6b00; max-width: 500px; }
            .icon { font-size: 4rem; margin-bottom: 20px; }
            .btn { background: #ff6b00; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="success-card">
            <div class="icon">✅</div>
            <h1>Booking Received!</h1>
            <p>Thank you for choosing Spruce Up Wash! We'll contact you within 24 hours.</p>
            <a href="/" class="btn">Back to Home</a>
            <a href="/reviews" class="btn">Leave a Review</a>
        </div>
    </body>
    </html>
    """

@app.route('/feedback')
def feedback():
    service_id = request.args.get('service_id', '')
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Feedback - Spruce Up Wash</title>
        <style>
            body { font-family: Arial, sans-serif; background: #1a0f0f; color: white; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; background: #2a1818; padding: 30px; border-radius: 15px; }
            .service-id { background: #1a0f0f; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Additional Feedback</h1>
            <p>Service ID: <span class="service-id">{service_id}</span></p>
            <p>Thank you for providing additional feedback. This helps us improve our services.</p>
            <p>Please email your detailed feedback to: <strong>spruceupwash@gmail.com</strong></p>
            <a href="/">Back to Home</a>
        </div>
    </body>
    </html>
    """

@app.route('/api/reviews')
def api_reviews():
    reviews = load_reviews()
    return jsonify(reviews[-6:][::-1])

# Initialize data files
def initialize_data_files():
    if not os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(SERVICE_IDS_FILE):
        with open(SERVICE_IDS_FILE, 'w') as f:
            json.dump({}, f)

if __name__ == '__main__':
    initialize_data_files()
    app.run(debug=True, host='0.0.0.0', port=5000)
