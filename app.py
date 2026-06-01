from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import os
import csv
from io import StringIO, BytesIO
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(os.path.dirname(__file__), 'admin_dashboard.html')

@app.route('/<path:filename>')
def serve_static(filename):
    root = os.path.dirname(__file__)
    file_path = os.path.join(root, filename)
    if os.path.exists(file_path):
        return send_from_directory(root, filename)
    return jsonify({'error': 'File not found'}), 404

# File to store bookings
BOOKINGS_FILE = 'bookings.json'

# ⚙️ OWNER CONFIGURATION - UPDATE THESE
OWNER_EMAIL = "your_email@gmail.com"  # Change this to owner's email
OWNER_WHATSAPP = "919876543210"  # Change this to owner's WhatsApp number
OWNER_NAME = "Adventure Trips Admin"

# ⚙️ GOOGLE SHEETS CONFIGURATION
GOOGLE_SERVICE_ACCOUNT_FILE = 'service_account.json'  # Place your service account JSON here
GOOGLE_SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'  # Replace with your Google Sheet ID
GOOGLE_SHEET_NAME = 'Bookings'  # Sheet tab name
GOOGLE_SHEET_HEADERS = [
    'Confirmation ID', 'Received At', 'Guardian Name', 'Guardian Mobile', 'Guardian WhatsApp',
    'Guardian Email', 'City', 'Emergency Contact', 'Amount Paid', 'UPI ID', 'Transaction ID',
    'Medical Info', 'Persons Count', 'Child Details'
]

def load_bookings():
    """Load bookings from JSON file"""
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_bookings(bookings):
    """Save bookings to JSON file"""
    with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def send_whatsapp_notification(booking_data):
    """Send WhatsApp notification to guardian (placeholder)"""
    guardian = booking_data['guardian']
    persons_count = booking_data.get('payment', {}).get('num_persons', booking_data.get('payment', {}).get('num_children', len(booking_data['children'])))
    
    message = f"""
✅ BOOKING CONFIRMATION

Guardian: {guardian['name']}
WhatsApp: {guardian['whatsapp']}
Email: {guardian['email']}

👥 Persons: {persons_count}
Amount Paid: ₹{booking_data['payment']['amount']}
Transaction ID: {booking_data['payment']['transaction_id']}

Trip: McLeodganj • Triund • Dharamkot
Dates: 19 June - 23 June 2026

Confirmation ID: {booking_data.get('confirmation_id', 'PENDING')}

Thank you for booking! We'll contact you soon.
    """
    
    print(f"\n{'='*60}")
    print("🔔 WHATSAPP MESSAGE SENT TO GUARDIAN:")
    print(f"{'='*60}")
    print(f"To: {guardian['whatsapp']}")
    print(message)
    print(f"{'='*60}\n")
    
    return message

def send_email_notification(booking_data):
    """Send email notification to guardian (placeholder)"""
    guardian = booking_data['guardian']
    
    email_subject = f"Booking Confirmation - McLeodganj Trip - {booking_data['confirmation_id']}"
    email_body = f"""
Dear {guardian['name']},

Your booking has been received and is pending verification.

Booking Details:
- Confirmation ID: {booking_data['confirmation_id']}
- Guardian Name: {guardian['name']}
- Contact: {guardian['whatsapp']} / {guardian['email']}
- City: {guardian['city']}

Persons Registered: {booking_data.get('payment', {}).get('num_persons', booking_data.get('payment', {}).get('num_children', len(booking_data['children'])))}
{chr(10).join([f"  {i+1}. Age: {child['age']}" for i, child in enumerate(booking_data['children'])])}

Payment Details:
- Amount Paid: ₹{booking_data['payment']['amount']}
- Transaction ID: {booking_data['payment']['transaction_id']}
- UPI ID Used: {booking_data['payment']['upi_id']}

Trip Details:
- Destination: McLeodganj • Triund • Dharamkot
- Dates: 19 June - 23 June 2026
- Min. Amount: ₹2,000 per person

We will verify your payment and confirm within 2 hours.
Contact us on WhatsApp for any queries.

Best regards,
Adventure Trips Team
    """
    
    print(f"\n{'='*60}")
    print("📧 EMAIL SENT TO GUARDIAN:")
    print(f"{'='*60}")
    print(f"To: {guardian['email']}")
    print(f"Subject: {email_subject}")
    print(email_body)
    print(f"{'='*60}\n")

def get_google_sheet_client():
    """Create and return a Google Sheets client."""
    if not os.path.exists(GOOGLE_SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Google service account file not found: {GOOGLE_SERVICE_ACCOUNT_FILE}")

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file'
    ]
    credentials = Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE, scopes=scopes)
    return gspread.authorize(credentials)


def append_booking_to_google_sheet(booking_data):
    """Append booking data to Google Sheet."""
    try:
        client = get_google_sheet_client()
        sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(GOOGLE_SHEET_NAME)

        # Ensure header row exists
        current_values = sheet.get_all_values()
        if not current_values or current_values[0] != GOOGLE_SHEET_HEADERS:
            sheet.clear()
            sheet.append_row(GOOGLE_SHEET_HEADERS)

        children_count = booking_data.get('payment', {}).get('num_persons', booking_data.get('payment', {}).get('num_children', len(booking_data['children'])))
        child_details = ' | '.join([
            f"Age: {child.get('age', '')}, Email: {child.get('email', '')}, Mobile: {child.get('mobile', '')}"
            for child in booking_data['children']
        ])

        row = [
            booking_data.get('confirmation_id', ''),
            booking_data.get('server_received_timestamp', ''),
            booking_data['guardian'].get('name', ''),
            booking_data['guardian'].get('mobile', ''),
            booking_data['guardian'].get('whatsapp', ''),
            booking_data['guardian'].get('email', ''),
            booking_data['guardian'].get('city', ''),
            booking_data['guardian'].get('emergency_contact', ''),
            booking_data['payment'].get('amount', ''),
            booking_data['payment'].get('upi_id', ''),
            booking_data['payment'].get('transaction_id', ''),
            booking_data.get('medical_info', ''),
            children_count,
            child_details
        ]
        sheet.append_row(row)
        print('✅ Booking appended to Google Sheet successfully.')
    except Exception as e:
        print(f'❌ Google Sheet append failed: {str(e)}')
        return str(e)


def send_owner_notification(booking_data):
    """Send notification to owner about new booking"""
    guardian = booking_data['guardian']
    persons_count = booking_data.get('payment', {}).get('num_persons', booking_data.get('payment', {}).get('num_children', len(booking_data['children'])))
    
    owner_message = f"""
🎉 NEW BOOKING RECEIVED!

Confirmation ID: {booking_data['confirmation_id']}
Time: {booking_data['server_received_timestamp']}

GUARDIAN DETAILS:
- Name: {guardian['name']}
- WhatsApp: {guardian['whatsapp']}
- Email: {guardian['email']}
- Mobile: {guardian['mobile']}
- City: {guardian['city']}

PERSONS: {persons_count}
{chr(10).join([f"  {i+1}. Age {child['age']} - {child['email'] if child['email'] != 'Not provided' else 'Email: Not provided'} - {child['mobile'] if child['mobile'] != 'Not provided' else 'Mobile: Not provided'}" for i, child in enumerate(booking_data['children'])])}

PAYMENT STATUS:
- Amount: ₹{booking_data['payment']['amount']}
- Transaction ID: {booking_data['payment']['transaction_id']}
- UPI ID: {booking_data['payment']['upi_id']}
- Status: ✅ Payment received (Pending verification)

Medical Info: {booking_data.get('medical_info', 'None')}

Google Sheet: https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}
    """
    
    print(f"\n{'='*70}")
    print("🔔 OWNER NOTIFICATION (WhatsApp & Email):")
    print(f"{'='*70}")
    print(owner_message)
    print(f"{'='*70}\n")
    
    # TODO: Integrate real email sending (SMTP) and WhatsApp (Twilio)
    # For now, just print to console
    return owner_message

@app.route('/api/bookings', methods=['POST'])
def receive_booking():
    """Receive booking data from form submission"""
    try:
        booking_data = request.get_json()
        
        # Generate confirmation ID
        import random
        import string
        confirmation_id = f"BK{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
        booking_data['confirmation_id'] = confirmation_id
        
        # Add server timestamp
        booking_data['server_received_timestamp'] = datetime.now().isoformat()
        
        # Load existing bookings
        bookings = load_bookings()
        
        # Add new booking
        bookings.append(booking_data)
        
        # Save to file
        save_bookings(bookings)
        
        # Append to Google Sheet
        append_booking_to_google_sheet(booking_data)
        
        # Send notifications
        send_whatsapp_notification(booking_data)
        send_email_notification(booking_data)
        send_owner_notification(booking_data)
        
        # Log to console
        print(f"\n🎉 NEW BOOKING RECEIVED - {confirmation_id}")
        print(f"Guardian: {booking_data['guardian']['name']}")
        print(f"Persons: {booking_data['payment'].get('num_persons', booking_data['payment'].get('num_children', len(booking_data['children'])))}")
        print(f"Amount: ₹{booking_data['payment']['amount']}")
        print(f"Time: {booking_data['server_received_timestamp']}\n")
        
        return jsonify({
            'success': True,
            'message': 'Booking received successfully',
            'confirmation_id': confirmation_id
        }), 201
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/bookings', methods=['GET'])
def get_all_bookings():
    """Get all bookings (for admin dashboard)"""
    bookings = load_bookings()
    return jsonify({
        'total_bookings': len(bookings),
        'total_amount': sum(float(b['payment']['amount']) for b in bookings),
        'bookings': bookings
    }), 200

@app.route('/api/bookings/<confirmation_id>', methods=['GET'])
def get_booking(confirmation_id):
    """Get specific booking by confirmation ID"""
    bookings = load_bookings()
    for booking in bookings:
        if booking.get('confirmation_id') == confirmation_id:
            return jsonify(booking), 200
    
    return jsonify({'error': 'Booking not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get booking statistics"""
    bookings = load_bookings()
    
    total_children = sum(b.get('payment', {}).get('num_persons', b.get('payment', {}).get('num_children', len(b.get('children', [])))) for b in bookings)
    total_amount = sum(float(b['payment']['amount']) for b in bookings)
    
    return jsonify({
        'total_bookings': len(bookings),
        'total_children': total_children,
        'total_amount': f"₹{total_amount:,.0f}",
        'average_per_booking': f"₹{total_amount/len(bookings):,.0f}" if bookings else "₹0",
        'last_booking': bookings[-1]['server_received_timestamp'] if bookings else None
    }), 200

@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export all bookings as JSON"""
    bookings = load_bookings()
    
    # Create JSON file
    json_data = json.dumps(bookings, ensure_ascii=False, indent=2)
    
    return jsonify({
        'filename': f'bookings_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
        'data': bookings
    }), 200

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export all bookings as CSV"""
    bookings = load_bookings()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Confirmation ID', 'Guardian Name', 'WhatsApp', 'Email', 'Mobile', 'City', 
                     'Persons Count', 'Amount Paid', 'Transaction ID', 'UPI ID', 'Date'])
    
    # Data
    for booking in bookings:
        writer.writerow([
            booking.get('confirmation_id', ''),
            booking['guardian']['name'],
            booking['guardian']['whatsapp'],
            booking['guardian']['email'],
            booking['guardian']['mobile'],
            booking['guardian']['city'],
            booking.get('payment', {}).get('num_persons', booking.get('payment', {}).get('num_children', len(booking['children']))),
            booking['payment']['amount'],
            booking['payment']['transaction_id'],
            booking['payment']['upi_id'],
            datetime.fromisoformat(booking['timestamp']).strftime('%d-%m-%Y %H:%M:%S')
        ])
    
    # Create file
    mem = BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'bookings_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/api/export/detailed-csv', methods=['GET'])
def export_detailed_csv():
    """Export all bookings with child details as CSV"""
    bookings = load_bookings()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Confirmation ID', 'Guardian Name', 'Guardian WhatsApp', 'Guardian Email', 
                     'Guardian Mobile', 'City', 'Child Number', 'Child Age', 'Child Email', 
                     'Child Mobile', 'Amount Paid', 'Transaction ID', 'UPI ID', 'Date', 'Medical Info'])
    
    # Data
    for booking in bookings:
        guardian = booking['guardian']
        children = booking['children']
        
        if not children:
            # Write guardian row even if no children
            writer.writerow([
                booking.get('confirmation_id', ''),
                guardian['name'],
                guardian['whatsapp'],
                guardian['email'],
                guardian['mobile'],
                guardian['city'],
                '',
                '',
                '',
                '',
                booking['payment']['amount'],
                booking['payment']['transaction_id'],
                booking['payment']['upi_id'],
                datetime.fromisoformat(booking['timestamp']).strftime('%d-%m-%Y %H:%M:%S'),
                booking.get('medical_info', '')
            ])
        else:
            # Write one row per child
            for i, child in enumerate(children, 1):
                writer.writerow([
                    booking.get('confirmation_id', ''),
                    guardian['name'],
                    guardian['whatsapp'],
                    guardian['email'],
                    guardian['mobile'],
                    guardian['city'],
                    i,
                    child['age'],
                    child['email'],
                    child['mobile'],
                    booking['payment']['amount'],
                    booking['payment']['transaction_id'],
                    booking['payment']['upi_id'],
                    datetime.fromisoformat(booking['timestamp']).strftime('%d-%m-%Y %H:%M:%S'),
                    booking.get('medical_info', '')
                ])
    
    # Create file
    mem = BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'bookings_detailed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   Adventure Trips - Booking System Backend             ║
    ║   McLeodganj • Triund • Dharamkot                      ║
    ╚════════════════════════════════════════════════════════╝
    
    🚀 Server running on http://localhost:{}
    📋 API Endpoints:
       POST   /api/bookings          - Submit new booking
       GET    /api/bookings          - Get all bookings
       GET    /api/bookings/<id>     - Get specific booking
       GET    /api/stats             - Get booking statistics
    
    💾 Data stored in: bookings.json
    """.format(port))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
