"""
STEP 2 - Configure Dynamic Email Template
Reads customers.csv and generates personalized email messages
for each customer based on their Service type.
Run this to preview emails before sending.
"""

import csv

# ─────────────────────────────────────────────
# Dynamic Email Template (configure once here)
# ─────────────────────────────────────────────
def generate_email(contact_name, service, company_name):
    """
    Generates a personalized email body.
    - contact_name : automatically filled from spreadsheet
    - service      : automatically filled (ISO 9001, ISO 14001, etc.)
    - company_name : automatically filled from spreadsheet
    """
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
# Preview all emails from the CSV
# ─────────────────────────────────────────────
def preview_all_emails(csv_file="customers.csv"):
    emails = []

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject, body = generate_email(
                contact_name=row["Contact Person Name"],
                service=row["Service"],
                company_name=row["Company Name"]
            )
            emails.append({
                "to": row["Contact Person Email"],
                "name": row["Contact Person Name"],
                "company": row["Company Name"],
                "service": row["Service"],
                "subject": subject,
                "body": body
            })

    print(f"✅ Step 2 Done! Generated {len(emails)} personalized emails.\n")
    print("=" * 60)
    for i, email in enumerate(emails, 1):
        print(f"\n📧 Email {i} — To: {email['to']}")
        print(f"Subject : {email['subject']}")
        print("-" * 40)
        print(email["body"])
        print("=" * 60)

    return emails


if __name__ == "__main__":
    preview_all_emails()
