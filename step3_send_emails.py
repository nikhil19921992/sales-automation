"""
STEP 3 - Automated Email Sending
Reads customers.csv, generates personalized emails, and sends them
using Gmail's SMTP server.

⚠️  SETUP REQUIRED BEFORE RUNNING:
────────────────────────────────────
1. Go to your Google Account → Security → 2-Step Verification (enable it)
2. Then go to: myaccount.google.com/apppasswords
3. Generate an App Password for "Mail"
4. Paste that 16-character password below as SENDER_APP_PASSWORD
5. Set SENDER_EMAIL to your Gmail address
"""

import csv
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────
# ⚙️  CONFIGURATION — Fill these in!
# ─────────────────────────────────────────────
SENDER_EMAIL       = "nikhilpc624@gmail.com"      # <-- YOUR Gmail address
SENDER_APP_PASSWORD = "dqiu oydf gclt bvvh"      # <-- 16-char App Password (NOT your real password)
SENDER_NAME        = "Sales Team"

# ─────────────────────────────────────────────
# Dynamic Email Template (same as Step 2)
# ─────────────────────────────────────────────
def generate_email(contact_name, service, company_name):
    subject = f"Your {service} Proposal – Action Required"
    body = f"""Hello {contact_name},

Your {service} proposal for {company_name} is expiring in 2 months.
Kindly get in touch with us to avail the best offers and support for renewal.

We value your continued trust in our services and would love to assist you
through the renewal process seamlessly.

Please reply to this email or call us at your convenience.

Regards,
Sales Team
"""
    return subject, body


# ─────────────────────────────────────────────
# Send one email via Gmail SMTP
# ─────────────────────────────────────────────
def send_email(smtp_server, to_email, subject, body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"]      = to_email

    # Plain text part
    msg.attach(MIMEText(body, "plain"))

    smtp_server.sendmail(SENDER_EMAIL, to_email, msg.as_string())


# ─────────────────────────────────────────────
# Main: Read CSV → Generate → Send
# ─────────────────────────────────────────────
def send_all_emails(csv_file="customers.csv"):
    # Load customer records
    customers = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row)

    print(f"📋 Loaded {len(customers)} customer records from '{csv_file}'")
    print(f"📤 Connecting to Gmail SMTP as {SENDER_EMAIL}...\n")

    success_count = 0
    fail_count    = 0

    # Connect to Gmail SMTP (port 587 with TLS)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()          # Encrypt the connection
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            print("✅ Login successful!\n")

            for i, customer in enumerate(customers, 1):
                name    = customer["Contact Person Name"]
                service = customer["Service"]
                company = customer["Company Name"]
                email   = customer["Contact Person Email"]

                subject, body = generate_email(name, service, company)

                try:
                    send_email(server, email, subject, body)
                    print(f"  [{i}/{len(customers)}] ✅ Sent → {name} ({company}) → {email}")
                    success_count += 1
                except Exception as e:
                    print(f"  [{i}/{len(customers)}] ❌ Failed → {email} | Error: {e}")
                    fail_count += 1

                # Small delay to avoid spam filters
                time.sleep(1)

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed!")
        print("   → Make sure you are using an App Password, NOT your real Gmail password.")
        print("   → Get one at: myaccount.google.com/apppasswords")
        return

    print(f"\n{'='*50}")
    print(f"✅ Done! Sent: {success_count} | Failed: {fail_count}")
    print(f"{'='*50}")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Safety check
    if SENDER_EMAIL == "your_gmail@gmail.com":
        print("⚠️  Please set your SENDER_EMAIL and SENDER_APP_PASSWORD before running!")
        print("   Open step3_send_emails.py and fill in the CONFIGURATION section.")
    else:
        send_all_emails()
