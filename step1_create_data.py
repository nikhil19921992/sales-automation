"""
STEP 1 - Import the Data
Creates a CSV spreadsheet with customer data.
Run this first to generate 'customers.csv'
"""

import csv

# Customer data (replace emails with your own test emails)
customers = [
    {
        "Company Name": "Santosh Chemical",
        "Service": "ISO 9001",
        "Contact Person Name": "Mr. Ajay Patel",
        "Contact Person Email": "truptinikhil7@gmail.com"  
    },
    {
        "Company Name": "Paritosh Engineering",
        "Service": "ISO 14001",
        "Contact Person Name": "Mr. Chirag Prajapati",
        "Contact Person Email": "nikhilchiniwal9616@gmail.com"  
    },
    {
        "Company Name": "Sintrex Fertilisers",
        "Service": "ISO 9001",
        "Contact Person Name": "Mr. Pritesh Shah",
        "Contact Person Email": "nikhilchiniwal9616@gmail.com"    
    },
    {
        "Company Name": "Ajay Precision Works",
        "Service": "ISO 20001",
        "Contact Person Name": "Mr. Jay Chauhan",
        "Contact Person Email": "nikhilchiniwal9616@gmail.com"  
    },
    {
        "Company Name": "Mega Mail Services",
        "Service": "ISO 45001",
        "Contact Person Name": "Mr. Dhiren Shah",
        "Contact Person Email": "nikhilchiniwal9616@gmail.com"  
    },
]

# Write to CSV
with open("customers.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Company Name", "Service", "Contact Person Name", "Contact Person Email"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(customers)

print("✅ Step 1 Done! 'customers.csv' created with", len(customers), "records.")
print("\nCustomers loaded:")
for c in customers:
    print(f"  - {c['Company Name']} | {c['Service']} | {c['Contact Person Name']}")
