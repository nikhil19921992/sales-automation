# 📧 Sales Automation — Personalized Email Sender

Automatically send personalized follow-up emails to customers based on their company name, contact person, and ISO service — all driven from a simple CSV spreadsheet.

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `step1_create_data.py` | Creates `customers.csv` with all customer records |
| `step2_email_template.py` | Previews all personalized emails before sending |
| `step3_send_emails.py` | Sends all emails automatically via Gmail |

---

## ✅ Requirements

- Python 3.x (no extra libraries needed — uses built-in modules only)
- A Gmail account with **2-Step Verification** enabled

---

## 🖥️ Installation & Setup

### Step 1 — Install Python

1. Go to [python.org/downloads](https://python.org/downloads)
2. Download the latest Python 3.x version
3. Run the installer
4. ⚠️ **Important:** Check the box that says **"Add Python to PATH"** before clicking Install

Verify installation — open **Command Prompt** and type:
```
python --version
```
You should see something like `Python 3.12.0`

---

### Step 2 — Download This Project

Click the green **Code** button on this GitHub page → **Download ZIP** → Extract it to your Desktop.

Or if you have Git installed:
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

---

### Step 3 — Open the Project Folder in Command Prompt

```
cd Desktop\YOUR_REPO_NAME
```

---

## ▶️ How to Run (Follow This Order)

---

### 🔵 Run Step 1 — Create Customer Data

1. Open `step1_create_data.py` in **Notepad**
2. Replace each `"your_test_email@gmail.com"` with the **actual email** of each customer:

```python
"Contact Person Email": "ajay.patel@gmail.com"       # Santosh Chemical
"Contact Person Email": "chirag.prajapati@gmail.com"  # Paritosh Engineering
"Contact Person Email": "pritesh.shah@gmail.com"      # Sintrex Fertilisers
"Contact Person Email": "jay.chauhan@gmail.com"       # Ajay Precision Works
"Contact Person Email": "dhiren.shah@gmail.com"       # Mega Mail Services
```

3. Save the file (`Ctrl + S`)
4. Run it:

```
python step1_create_data.py
```

✅ Expected output:
```
✅ Step 1 Done! 'customers.csv' created with 5 records.
```

A file called `customers.csv` will appear in the folder. You can open it in Excel to verify.

---

### 🟡 Run Step 2 — Preview Emails (No Emails Sent Yet)

```
python step2_email_template.py
```

✅ Expected output — all 5 emails printed in the terminal, each with the correct name and ISO service filled in automatically:

```
📧 Email 1 — To: ajay.patel@gmail.com
Subject : Your ISO 9001 Proposal – Action Required
----------------------------------------
Hello Mr. Ajay Patel,

Your ISO 9001 proposal for Santosh Chemical is expiring in 2 months...
```

No emails are sent at this step. This is just a preview.

---

### 🔑 One-Time Gmail Setup — Get Your App Password

Gmail does not allow scripts to use your real password. You need a special **App Password**.

1. Make sure **2-Step Verification** is ON:
   - Go to [myaccount.google.com](https://myaccount.google.com)
   - Click **Security** → **2-Step Verification** → Turn it on

2. Generate an App Password:
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Under "App name", type `SalesAutomation`
   - Click **Create**
   - Copy the **16-character password** shown (e.g. `abcd efgh ijkl mnop`)
   - ⚠️ Save it — you won't see it again

---

### 🟢 Run Step 3 — Send All Emails

1. Open `step3_send_emails.py` in **Notepad**
2. Fill in your credentials at the top of the file:

```python
SENDER_EMAIL        = "yourname@gmail.com"       # Your Gmail address
SENDER_APP_PASSWORD = "abcd efgh ijkl mnop"      # 16-char App Password from above
```

3. Save the file (`Ctrl + S`)
4. Run it:

```
python step3_send_emails.py
```

✅ Expected output:
```
📋 Loaded 5 customer records from 'customers.csv'
📤 Connecting to Gmail SMTP as yourname@gmail.com...

✅ Login successful!

  [1/5] ✅ Sent → Mr. Ajay Patel (Santosh Chemical) → ajay.patel@gmail.com
  [2/5] ✅ Sent → Mr. Chirag Prajapati (Paritosh Engineering) → chirag.prajapati@gmail.com
  [3/5] ✅ Sent → Mr. Pritesh Shah (Sintrex Fertilisers) → pritesh.shah@gmail.com
  [4/5] ✅ Sent → Mr. Jay Chauhan (Ajay Precision Works) → jay.chauhan@gmail.com
  [5/5] ✅ Sent → Mr. Dhiren Shah (Mega Mail Services) → dhiren.shah@gmail.com

==================================================
✅ Done! Sent: 5 | Failed: 0
==================================================
```

Each customer receives a **personalized email** with their own name and ISO service automatically inserted.

---

## 📬 What the Email Looks Like

**Subject:** Your ISO 9001 Proposal – Action Required

```
Hello Mr. Ajay Patel,

Your ISO 9001 proposal for Santosh Chemical is expiring in 2 months.
Kindly get in touch with us to avail the best offers and support for renewal.

We value your continued trust in our services and would love to assist you
through the renewal process seamlessly.

Please reply to this email or call us at your convenience.

Regards,
Sales Team
```

The **name**, **ISO service**, and **company name** change automatically for every customer.

---

## ❌ Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `python is not recognized` | Python not in PATH | Reinstall Python, check "Add to PATH" |
| `Authentication failed` | Used real Gmail password | Use the 16-char App Password instead |
| `No such file: customers.csv` | Step 1 not run yet | Run `step1_create_data.py` first |
| App Passwords option missing | 2-Step Verification is OFF | Enable 2-Step Verification first |
| Emails going to Spam | First-time sender | Check Spam folder and mark as "Not Spam" |

---

## 💡 How to Add More Customers

1. Open `step1_create_data.py`
2. Add a new entry inside the `customers = [...]` list:

```python
{
    "Company Name": "New Company Ltd",
    "Service": "ISO 9001",
    "Contact Person Name": "Mr. New Person",
    "Contact Person Email": "newperson@gmail.com"
},
```

3. Save and re-run `step1_create_data.py` then `step3_send_emails.py`

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Libraries:** `csv`, `smtplib`, `email` — all built into Python, nothing to install
- **Email Provider:** Gmail SMTP (port 587 with TLS encryption)
