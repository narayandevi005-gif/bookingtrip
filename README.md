# 🏔️ Adventure Trips - Booking System
## McLeodganj • Triund • Dharamkot

### Features

✅ **Children Booking Form**
- Guardian/Booking person details
- Multiple children registration with names, ages, emails, mobile numbers
- Remove Aadhar/ID details requirement
- Medical information field

✅ **UPI Payment Integration**
- UPI payment method for participants
- Payment screenshot upload
- Transaction ID verification
- Minimum booking amount: ₹2,000 per person

✅ **Real-time Data Logging**
- All booking data automatically logged
- WhatsApp notification sent to guardian
- WhatsApp + Email notifications sent to OWNER on every booking
- Browser local storage backup
- JSON file persistence

✅ **Data Export (Owner Dashboard)**
- Export all bookings as JSON
- Export as CSV (summary format)
- Export as Detailed CSV (with child details)
- Download anytime from admin dashboard

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
python app.py
```
The server will run on `http://localhost:5000`

### 3. Open the Form in Browser
Open `index.html` in your web browser:
```bash
# On Windows:
start index.html

# Or manually open: c:\Users\as\PYTHON\index.html
```

---

## 📋 Form Sections

### Guardian Details
- Full Name (required)
- Mobile Number (required)
- WhatsApp Number (required)
- Email Address (required)
- City (required)
- Emergency Contact

### Children/Participants
- Single child entry per booking
- Each child needs:
  - Age (required, 1-18)
  - Email (optional)
  - Mobile Number (optional)

### Payment Details
- UPI ID used for payment (required)
- Transaction ID/UTR (required)
- Payment screenshot upload (required)
- Amount paid in ₹ (minimum ₹2,000)

---

## 💾 Data Management

### Booking Data Flow
1. User fills form and submits
2. Data sent to backend via `/api/bookings`
3. Confirmation ID generated (e.g., BKABCD1234)
4. Data saved to `bookings.json`
5. WhatsApp & Email notifications prepared
6. Data also saved in browser localStorage

### Access Bookings
```bash
# View all bookings (in browser console or via API)
# GET http://localhost:5000/api/bookings

# Get specific booking
# GET http://localhost:5000/api/bookings/BKABCD1234

# Get statistics
# GET http://localhost:5000/api/stats
```

---

## 📱 UPI Payment Instructions (in form)

1. Pay ₹2,000 per person via UPI to: **8447919303@ptsbi**
2. Take screenshot of payment confirmation
3. Upload screenshot in form
4. Enter UPI ID and Transaction ID
5. Submit form

**Update the UPI ID**: Edit `index.html` to use your actual UPI ID

---

## � Notifications Setup

### ✅ What's Ready Now
- **Console Notifications**: All notifications print in Flask server console
- **Data Logging**: All bookings auto-saved to `bookings.json`
- **Admin Dashboard**: View all bookings in real-time with auto-refresh (30 sec)

### 📧 Email Notifications to Owner

**Currently**: Notifications print in Flask console

**To Enable Real Email Sending:**

1. **Using Gmail (Easy):**
   ```python
   # Add to app.py imports:
   import smtplib
   from email.mime.text import MIMEText
   from email.mime.multipart import MIMEMultipart
   
   # Add function in app.py:
   def send_owner_email(subject, message):
       sender_email = "your_gmail@gmail.com"
       sender_password = "your_app_password"  # App password, not Gmail password
       receiver_email = OWNER_EMAIL
       
       msg = MIMEMultipart()
       msg['From'] = sender_email
       msg['To'] = receiver_email
       msg['Subject'] = subject
       msg.attach(MIMEText(message, 'plain'))
       
       with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
           server.login(sender_email, sender_password)
           server.send_message(msg)
   ```

2. **Using Twilio (WhatsApp):**
   - Get Twilio account (https://www.twilio.com)
   - Install: `pip install twilio`
   - Add WhatsApp sending code in `send_owner_notification()`

### 📊 Data Export Options

**Three ways to download booking data:**

1. **Download JSON** - Complete raw data in JSON format
2. **Download CSV** - Summary view (one row per booking)
3. **Download Detailed CSV** - Full details (one row per child)

All available in admin dashboard buttons!

---

## 🔍 How It Works

### When a Child Submits Booking:
1. Child fills form → Submits data + payment screenshot
2. Backend receives and validates (minimum ₹2,000)
3. Generates unique Confirmation ID
4. Saves to `bookings.json`
5. **Owner gets notification in Flask console** (real-time):
   - Guardian details
   - Children count & ages
   - Payment amount & transaction ID
   - Medical information
6. Guardian gets confirmation message
7. Owner can instantly download data from admin dashboard

### Real-time Viewing:
- **Flask Console**: See new bookings immediately as they arrive
- **Admin Dashboard**: Auto-refreshes every 30 seconds
- **bookings.json**: All data persistently saved
- **Export Options**: Download data anytime in JSON/CSV format

---

## 📊 Data Fields Captured

Each booking includes:
- **Guardian**: Name, Mobile, WhatsApp, Email, City, Emergency Contact
- **Children**: Age, Email, Mobile
- **Payment**: UPI ID, Transaction ID, Amount, Timestamp

---

## 🚀 GitHub + Render Deployment

This project is ready for GitHub so you can deploy it directly to Render.

1. Create a GitHub repository for this project.
2. In your project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. On Render, create a new Web Service and connect it to this GitHub repo.
4. Use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. After deploy, open the service URL and your booking form will appear.

### Notes
- The `Procfile` and `render.yaml` are already included for Render.
- If you want a custom domain like `bookingtripform.site.je`, add it in Render's Custom Domains settings.
- Keep `service_account.json` and other secrets out of GitHub if you add Google Sheets integration later.

- **Medical Info**: Any medical conditions or allergies
- **Confirmation ID**: Unique booking reference
- **Server Timestamp**: When booking was received

---

## 🔧 Configuration

### Owner Contact Details
Edit in `app.py` (Lines 14-16):
```python
OWNER_EMAIL = "your_email@gmail.com"        # Your email for notifications
OWNER_WHATSAPP = "919876543210"            # Your WhatsApp number (with country code)
OWNER_NAME = "Adventure Trips Admin"       # Your name
```

### Google Sheets Setup
1. Create a Google Sheet and copy its Sheet ID from the URL.
2. Create a Google Cloud service account and enable the Google Sheets API.
3. Download the service account JSON file and save it as `service_account.json` in the `PYTHON/` folder.
4. Share the Google Sheet with the service account email address shown in the JSON.
5. Update `app.py` with your sheet details:
```python
GOOGLE_SERVICE_ACCOUNT_FILE = 'service_account.json'
GOOGLE_SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'
GOOGLE_SHEET_NAME = 'Bookings'
```

### Minimum Booking Amount
Edit in `index.html` (Line ~33):
```html
<div class="price">₹2,000</div>
```

### Trip Details
Edit in `index.html`:
- Trip dates
- Destinations
- Itinerary
- Emergency contact requirements

### Backend Port
Edit in `app.py` (Last line):
```python
app.run(debug=True, host='localhost', port=5000)  # Change port here
```

---

## 📁 File Structure

```
PYTHON/
├── index.html           # Main booking form (open in browser)
├── app.py               # Flask backend server
├── requirements.txt     # Python dependencies
├── bookings.json        # All saved bookings
└── README.md           # This file
```

---

## 🔒 Security Notes

⚠️ **Before going live:**
1. Hide payment screenshots (store securely)
2. Validate UPI transactions on backend
3. Use HTTPS for production
4. Add authentication for admin dashboard
5. Encrypt sensitive data
6. Set up proper error handling
7. Add CSRF protection

---

## 🆘 Troubleshooting

### Backend not receiving data?
- Ensure `app.py` is running on port 5000
- Check browser console for CORS errors
- Open `http://localhost:5000/api/stats` to verify server

### Data not saving?
- Check `bookings.json` permissions
- Verify Flask is running
- Check browser localStorage (F12 > Application > Local Storage)

### Notifications not sending?
- WhatsApp/Email features need API setup (see above)
- Check console logs for errors
- Update with actual Twilio/SMTP credentials

---

## 📞 Support

For queries or issues:
1. Check the browser console (F12)
2. Review `bookings.json` for submission history
3. Verify Flask server is running: `python app.py`
4. Check WhatsApp/Email logs in Flask console

---

## 📝 License & Usage
For personal/commercial use. Update branding as needed.

**Last Updated**: June 1, 2026
