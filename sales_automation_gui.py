"""
SALES AUTOMATION — GUI App with Auto-Save
Run: python sales_automation_gui.py

Everything is saved automatically to 'sales_data.json' in the same folder.
Next time you open the app, all customers and Gmail settings are restored.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json, os, smtplib, time, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Save file lives next to the script ──────────────────────────
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales_data.json")

DEFAULT_CUSTOMERS = [
    {"Company Name": "Santosh Chemical",     "Service": "ISO 9001",  "Contact Person Name": "Mr. Ajay Patel",       "Contact Person Email": ""},
    {"Company Name": "Paritosh Engineering", "Service": "ISO 14001", "Contact Person Name": "Mr. Chirag Prajapati", "Contact Person Email": ""},
    {"Company Name": "Sintrex Fertilisers",  "Service": "ISO 9001",  "Contact Person Name": "Mr. Pritesh Shah",     "Contact Person Email": ""},
    {"Company Name": "Ajay Precision Works", "Service": "ISO 20001", "Contact Person Name": "Mr. Jay Chauhan",      "Contact Person Email": ""},
    {"Company Name": "Mega Mail Services",   "Service": "ISO 45001", "Contact Person Name": "Mr. Dhiren Shah",      "Contact Person Email": ""},
]

# ================================================================
#  SAVE / LOAD
# ================================================================
def load_data():
    """Load saved data from JSON, or return defaults if first run."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception:
            pass
    return {
        "customers": [dict(c) for c in DEFAULT_CUSTOMERS],
        "gmail": {"sender_name": "Sales Team", "sender_email": "", "app_password": ""}
    }

def save_data(customers, gmail):
    """Save all current data to JSON immediately."""
    data = {"customers": customers, "gmail": gmail}
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ================================================================
#  EMAIL TEMPLATE
# ================================================================
def generate_email(name, service, company):
    subject = f"Your {service} Proposal – Action Required"
    body = (
        f"Hello {name},\n\n"
        f"Your {service} proposal for {company} is expiring in 2 months.\n"
        f"Kindly get in touch with us to avail the best offers and support for renewal.\n\n"
        f"We value your continued trust in our services and would love to assist you "
        f"through the renewal process seamlessly.\n\n"
        f"Please reply to this email or call us at your convenience.\n\n"
        f"Regards,\nSales Team"
    )
    return subject, body

# ================================================================
#  MAIN APP
# ================================================================
class SalesAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Automation — Email Sender")
        self.root.geometry("960x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#F0F4FF")

        # Colours
        self.C = {
            "bg":     "#F0F4FF",
            "card":   "#FFFFFF",
            "blue":   "#2563EB",
            "green":  "#16A34A",
            "red":    "#DC2626",
            "navy":   "#1E3A8A",
            "text":   "#1E293B",
            "muted":  "#64748B",
            "border": "#CBD5E1",
            "row1":   "#EFF6FF",
            "row2":   "#FFFFFF",
            "saved":  "#DCFCE7",
        }

        # Load saved data
        saved = load_data()
        self.customers = saved["customers"]
        self.gmail_saved = saved["gmail"]

        self._build_ui()

        # Auto-save on any window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── SAVE TRIGGER ─────────────────────────────────────────────
    def _autosave(self):
        """Sync UI → memory → disk silently."""
        self._sync_emails_from_ui()
        gmail = {
            "sender_name":  self.gmail_entries["Sender Name"].get().strip(),
            "sender_email": self.gmail_entries["Gmail Address"].get().strip(),
            "app_password": self.gmail_entries["App Password"].get().strip(),
        }
        save_data(self.customers, gmail)
        self._flash_saved()

    def _flash_saved(self):
        """Briefly show a green 'Saved ✓' indicator."""
        self.save_lbl.configure(text="  ✅ Saved", fg=self.C["green"])
        self.root.after(2000, lambda: self.save_lbl.configure(text="", fg=self.C["bg"]))

    def _on_close(self):
        self._autosave()
        self.root.destroy()

    # ── UI BUILDER ────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=self.C["navy"], pady=14)
        hdr.pack(fill="x")

        hdr_inner = tk.Frame(hdr, bg=self.C["navy"])
        hdr_inner.pack(fill="x", padx=20)

        tk.Label(hdr_inner, text="📧  Sales Automation",
                 font=("Segoe UI", 19, "bold"),
                 bg=self.C["navy"], fg="white").pack(side="left")

        self.save_lbl = tk.Label(hdr_inner, text="",
                                  font=("Segoe UI", 10, "bold"),
                                  bg=self.C["navy"], fg=self.C["bg"])
        self.save_lbl.pack(side="right", padx=8)

        tk.Button(hdr_inner, text="💾  Save Now",
                  font=("Segoe UI", 9, "bold"),
                  bg="#3B82F6", fg="white", relief="flat",
                  padx=10, pady=4, cursor="hand2",
                  command=self._autosave).pack(side="right")

        tk.Label(hdr, text="All changes are saved automatically",
                 font=("Segoe UI", 9),
                 bg=self.C["navy"], fg="#93C5FD").pack()

        # Tabs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",     background=self.C["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"),
                        padding=[16, 8], background="#D1D5DB", foreground=self.C["text"])
        style.map("TNotebook.Tab",
                  background=[("selected", self.C["blue"])],
                  foreground=[("selected", "white")])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=16, pady=10)

        self.tab1 = tk.Frame(nb, bg=self.C["bg"])
        self.tab2 = tk.Frame(nb, bg=self.C["bg"])
        self.tab3 = tk.Frame(nb, bg=self.C["bg"])

        nb.add(self.tab1, text="  👥 Step 1 — Customers  ")
        nb.add(self.tab2, text="  🔑 Step 2 — Gmail Setup  ")
        nb.add(self.tab3, text="  📤 Step 3 — Send Emails  ")

        self._build_tab1()
        self._build_tab2()
        self._build_tab3()

    # ── TAB 1: CUSTOMERS ─────────────────────────────────────────
    def _build_tab1(self):
        t = self.tab1

        top = tk.Frame(t, bg=self.C["bg"])
        top.pack(fill="x", padx=16, pady=(10,2))
        tk.Label(top, text="Customer List",
                 font=("Segoe UI", 13, "bold"),
                 bg=self.C["bg"], fg=self.C["navy"]).pack(side="left")
        self.count_lbl = tk.Label(top, text=f"({len(self.customers)} customers)",
                                   font=("Segoe UI", 9),
                                   bg=self.C["bg"], fg=self.C["muted"])
        self.count_lbl.pack(side="left", padx=8)

        tk.Label(t,
                 text="Type each customer's email in the Email column — it saves automatically.",
                 font=("Segoe UI", 9), bg=self.C["bg"], fg=self.C["muted"]
                 ).pack(anchor="w", padx=16)

        # Table
        tbl_outer = tk.Frame(t, bg=self.C["card"],
                             highlightthickness=1,
                             highlightbackground=self.C["border"])
        tbl_outer.pack(fill="both", expand=True, padx=16, pady=8)

        # Column header
        cols      = ["#", "Company Name", "Service", "Contact Person Name", "Email Address", ""]
        col_chars = [3,    22,             11,         22,                    28,               5]
        hdr_fr = tk.Frame(tbl_outer, bg=self.C["blue"])
        hdr_fr.pack(fill="x")
        for col, w in zip(cols, col_chars):
            tk.Label(hdr_fr, text=col, font=("Segoe UI", 9, "bold"),
                     bg=self.C["blue"], fg="white",
                     width=w, anchor="w", padx=6, pady=7).pack(side="left")

        # Scrollable body
        canvas = tk.Canvas(tbl_outer, bg=self.C["card"], highlightthickness=0)
        sb = ttk.Scrollbar(tbl_outer, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas, bg=self.C["card"])
        self.rows_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.email_vars = []
        self._render_rows()

        # Add New Customer form
        add_card = tk.Frame(t, bg=self.C["card"],
                            highlightthickness=1,
                            highlightbackground=self.C["border"])
        add_card.pack(fill="x", padx=16, pady=(0, 10))

        tk.Label(add_card, text="➕  Add New Customer",
                 font=("Segoe UI", 10, "bold"),
                 bg=self.C["card"], fg=self.C["navy"]).grid(
                     row=0, column=0, columnspan=9,
                     sticky="w", padx=12, pady=(10, 4))

        field_defs = [("Company Name", 16), ("Service", 10),
                      ("Contact Name", 16), ("Email", 22)]
        self.new_entries = {}
        for i, (lbl, w) in enumerate(field_defs):
            tk.Label(add_card, text=lbl, font=("Segoe UI", 9),
                     bg=self.C["card"], fg=self.C["muted"]).grid(
                         row=1, column=i*2, sticky="w", padx=(12,2), pady=8)
            e = tk.Entry(add_card, font=("Segoe UI", 9), width=w,
                         relief="solid", bd=1,
                         highlightthickness=1,
                         highlightbackground=self.C["border"])
            e.grid(row=1, column=i*2+1, sticky="ew", padx=(0, 8), pady=8)
            self.new_entries[lbl] = e

        tk.Button(add_card, text="Add & Save",
                  font=("Segoe UI", 9, "bold"),
                  bg=self.C["blue"], fg="white", relief="flat",
                  padx=12, pady=5, cursor="hand2",
                  command=self._add_customer).grid(
                      row=1, column=8, padx=8, pady=8)

    def _render_rows(self):
        for w in self.rows_frame.winfo_children():
            w.destroy()
        self.email_vars = []

        for i, c in enumerate(self.customers):
            bg = self.C["row1"] if i % 2 == 0 else self.C["row2"]
            row = tk.Frame(self.rows_frame, bg=bg)
            row.pack(fill="x")

            tk.Label(row, text=str(i+1), font=("Segoe UI", 9),
                     bg=bg, fg=self.C["muted"],
                     width=3, padx=6, pady=8).pack(side="left")
            tk.Label(row, text=c["Company Name"], font=("Segoe UI", 9),
                     bg=bg, fg=self.C["text"],
                     width=22, anchor="w", padx=4).pack(side="left")
            tk.Label(row, text=c["Service"], font=("Segoe UI", 9, "bold"),
                     bg=bg, fg=self.C["blue"],
                     width=11, anchor="w", padx=4).pack(side="left")
            tk.Label(row, text=c["Contact Person Name"], font=("Segoe UI", 9),
                     bg=bg, fg=self.C["text"],
                     width=22, anchor="w", padx=4).pack(side="left")

            email_var = tk.StringVar(value=c["Contact Person Email"])
            # Auto-save whenever the email field loses focus
            email_entry = tk.Entry(row, textvariable=email_var,
                                   font=("Segoe UI", 9), width=28,
                                   relief="solid", bd=1,
                                   highlightthickness=1,
                                   highlightbackground=self.C["border"])
            email_entry.pack(side="left", padx=6, pady=5)
            email_entry.bind("<FocusOut>", lambda e: self._autosave())
            email_entry.bind("<Return>",   lambda e: self._autosave())
            self.email_vars.append(email_var)

            idx = i
            tk.Button(row, text="✕",
                      font=("Segoe UI", 8, "bold"),
                      bg="#FEE2E2", fg=self.C["red"],
                      relief="flat", padx=5, cursor="hand2",
                      command=lambda x=idx: self._delete_customer(x)
                      ).pack(side="left", padx=4)

        # Update count label
        if hasattr(self, "count_lbl"):
            self.count_lbl.configure(text=f"({len(self.customers)} customers)")

    def _add_customer(self):
        vals = {k: e.get().strip() for k, e in self.new_entries.items()}
        if not all(vals.values()):
            messagebox.showwarning("Missing Info",
                "Please fill in all 4 fields before adding.")
            return
        self.customers.append({
            "Company Name":         vals["Company Name"],
            "Service":              vals["Service"],
            "Contact Person Name":  vals["Contact Name"],
            "Contact Person Email": vals["Email"]
        })
        for e in self.new_entries.values():
            e.delete(0, "end")
        self._render_rows()
        self._autosave()   # ← save immediately after adding
        messagebox.showinfo("Saved ✅",
            f"'{vals['Company Name']}' added and saved!\n"
            "They will appear next time you open the app.")

    def _delete_customer(self, idx):
        name = self.customers[idx]["Company Name"]
        if messagebox.askyesno("Delete Customer",
                f"Remove '{name}' from the list?\nThis cannot be undone."):
            self.customers.pop(idx)
            self._render_rows()
            self._autosave()   # ← save immediately after deleting

    # ── TAB 2: GMAIL SETUP ───────────────────────────────────────
    def _build_tab2(self):
        t = self.tab2

        tk.Label(t, text="Gmail Configuration",
                 font=("Segoe UI", 13, "bold"),
                 bg=self.C["bg"], fg=self.C["navy"]).pack(
                     anchor="w", padx=16, pady=(12, 4))
        tk.Label(t, text="Your credentials are saved locally and loaded automatically next time.",
                 font=("Segoe UI", 9),
                 bg=self.C["bg"], fg=self.C["muted"]).pack(anchor="w", padx=16)

        card = tk.Frame(t, bg=self.C["card"],
                        highlightthickness=1,
                        highlightbackground=self.C["border"])
        card.pack(fill="x", padx=16, pady=12)
        card.columnconfigure(1, weight=1)

        fields = [
            ("Sender Name",    self.gmail_saved.get("sender_name", "Sales Team"), False),
            ("Gmail Address",  self.gmail_saved.get("sender_email", ""),          False),
            ("App Password",   self.gmail_saved.get("app_password", ""),          True),
        ]
        self.gmail_entries = {}
        for i, (lbl, default, hide) in enumerate(fields):
            tk.Label(card, text=lbl,
                     font=("Segoe UI", 10, "bold"),
                     bg=self.C["card"], fg=self.C["text"]).grid(
                         row=i, column=0, sticky="w", padx=16, pady=12)
            e = tk.Entry(card, font=("Segoe UI", 10), width=42,
                         relief="solid", bd=1,
                         show="●" if hide else "",
                         highlightthickness=1,
                         highlightbackground=self.C["border"])
            if default:
                e.insert(0, default)
            e.grid(row=i, column=1, sticky="ew", padx=(0, 16), pady=12)
            # Auto-save when focus leaves any Gmail field
            e.bind("<FocusOut>", lambda ev: self._autosave())
            e.bind("<Return>",   lambda ev: self._autosave())
            self.gmail_entries[lbl] = e

        # Saved indicator in card
        tk.Label(card,
                 text="🔒  Credentials are saved locally on your PC only (sales_data.json)",
                 font=("Segoe UI", 8), bg=self.C["card"],
                 fg=self.C["muted"]).grid(
                     row=3, column=0, columnspan=2,
                     sticky="w", padx=16, pady=(0, 10))

        # Help box
        help_fr = tk.Frame(t, bg="#EFF6FF",
                           highlightthickness=1,
                           highlightbackground="#BFDBFE")
        help_fr.pack(fill="x", padx=16, pady=4)
        tk.Label(help_fr,
                 text=(
                     "🔑  How to get your App Password (one-time setup):\n"
                     "  1. Go to myaccount.google.com → Security → 2-Step Verification → Turn ON\n"
                     "  2. Go to myaccount.google.com/apppasswords\n"
                     "  3. Type 'SalesAutomation' → Click Create → Copy the 16-character password\n"
                     "  4. Paste it in the App Password field above — it will be saved automatically"
                 ),
                 font=("Segoe UI", 9),
                 bg="#EFF6FF", fg="#1D4ED8",
                 justify="left", anchor="w").pack(padx=14, pady=12)

    # ── TAB 3: PREVIEW & SEND ─────────────────────────────────────
    def _build_tab3(self):
        t = self.tab3

        tk.Label(t, text="Preview & Send Emails",
                 font=("Segoe UI", 13, "bold"),
                 bg=self.C["bg"], fg=self.C["navy"]).pack(
                     anchor="w", padx=16, pady=(12, 2))
        tk.Label(t, text="Preview all emails first, then click Send.",
                 font=("Segoe UI", 9),
                 bg=self.C["bg"], fg=self.C["muted"]).pack(anchor="w", padx=16)

        btn_fr = tk.Frame(t, bg=self.C["bg"])
        btn_fr.pack(fill="x", padx=16, pady=10)

        tk.Button(btn_fr, text="🔍  Preview Emails",
                  font=("Segoe UI", 10, "bold"),
                  bg="#6366F1", fg="white", relief="flat",
                  padx=20, pady=8, cursor="hand2",
                  command=self._preview_emails).pack(side="left", padx=(0, 10))

        self.send_btn = tk.Button(btn_fr, text="📤  Send All Emails",
                                   font=("Segoe UI", 10, "bold"),
                                   bg=self.C["green"], fg="white",
                                   relief="flat", padx=20, pady=8,
                                   cursor="hand2", state="disabled",
                                   command=self._send_emails)
        self.send_btn.pack(side="left")

        self.preview_text = scrolledtext.ScrolledText(
            t, font=("Courier New", 9), wrap="word",
            bg="#F8FAFF", fg=self.C["text"],
            relief="solid", bd=1, height=18, state="disabled")
        self.preview_text.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        self.status_var = tk.StringVar(value="Ready — click Preview Emails to start.")
        tk.Label(t, textvariable=self.status_var,
                 font=("Segoe UI", 9), bg="#E2E8F0",
                 fg=self.C["muted"], anchor="w",
                 padx=12, pady=5).pack(fill="x", padx=16, pady=(0, 4))

        self.progress = ttk.Progressbar(t, mode="determinate")
        self.progress.pack(fill="x", padx=16, pady=(0, 10))

    # ── SYNC / PREVIEW / SEND ─────────────────────────────────────
    def _sync_emails_from_ui(self):
        for i, var in enumerate(self.email_vars):
            if i < len(self.customers):
                self.customers[i]["Contact Person Email"] = var.get().strip()

    def _preview_emails(self):
        self._sync_emails_from_ui()
        missing = [c["Company Name"] for c in self.customers
                   if not c["Contact Person Email"]]
        if missing:
            messagebox.showwarning("Missing Emails",
                "Please fill in email addresses for:\n" +
                "\n".join(f"  • {m}" for m in missing))
            return

        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        for i, c in enumerate(self.customers, 1):
            subject, body = generate_email(
                c["Contact Person Name"], c["Service"], c["Company Name"])
            self.preview_text.insert("end",
                f"{'─'*62}\n"
                f"📧  Email {i} of {len(self.customers)}\n"
                f"  To      : {c['Contact Person Email']}\n"
                f"  Subject : {subject}\n"
                f"{'─'*62}\n"
                f"{body}\n\n")
        self.preview_text.configure(state="disabled")
        self.send_btn.configure(state="normal")
        self.status_var.set(
            f"✅ {len(self.customers)} emails previewed — click Send All Emails to deliver.")

    def _send_emails(self):
        sender_name  = self.gmail_entries["Sender Name"].get().strip()
        sender_email = self.gmail_entries["Gmail Address"].get().strip()
        app_password = self.gmail_entries["App Password"].get().strip()

        if not sender_email:
            messagebox.showwarning("Missing Info",
                "Please enter your Gmail address in Step 2.")
            return
        if not app_password:
            messagebox.showwarning("Missing Info",
                "Please enter your App Password in Step 2.")
            return
        if not messagebox.askyesno("Confirm Send",
            f"Send {len(self.customers)} personalized emails now?\n\n"
            "This will deliver real emails to all customers listed."):
            return

        self.send_btn.configure(state="disabled")
        self.progress["value"]   = 0
        self.progress["maximum"] = len(self.customers)

        def do_send():
            success = failed = 0
            log = []
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.login(sender_email, app_password)

                    for i, c in enumerate(self.customers, 1):
                        subject, body = generate_email(
                            c["Contact Person Name"],
                            c["Service"], c["Company Name"])
                        msg = MIMEMultipart("alternative")
                        msg["Subject"] = subject
                        msg["From"]    = f"{sender_name} <{sender_email}>"
                        msg["To"]      = c["Contact Person Email"]
                        msg.attach(MIMEText(body, "plain"))
                        try:
                            server.sendmail(sender_email,
                                            c["Contact Person Email"],
                                            msg.as_string())
                            success += 1
                            entry = f"✅  [{i}/{len(self.customers)}] {c['Contact Person Name']} → {c['Contact Person Email']}"
                        except Exception as ex:
                            failed += 1
                            entry = f"❌  [{i}/{len(self.customers)}] {c['Contact Person Email']} — {ex}"
                        log.append(entry)
                        self.root.after(0, lambda v=i: self.progress.configure(value=v))
                        self.root.after(0, lambda s=entry: self.status_var.set(s))
                        time.sleep(1)

            except smtplib.SMTPAuthenticationError:
                self.root.after(0, lambda: messagebox.showerror(
                    "Authentication Failed",
                    "Gmail login failed.\n\n"
                    "→ Use an App Password, NOT your real Gmail password.\n"
                    "→ Get one at: myaccount.google.com/apppasswords"))
                self.root.after(0, lambda: self.send_btn.configure(state="normal"))
                return

            summary = (
                f"\n{'═'*62}\n"
                f"  SENDING COMPLETE\n"
                f"  ✅ Sent   : {success}\n"
                f"  ❌ Failed : {failed}\n"
                f"{'═'*62}\n\n" + "\n".join(log)
            )

            def finish():
                self.preview_text.configure(state="normal")
                self.preview_text.insert("end", summary)
                self.preview_text.configure(state="disabled")
                self.preview_text.see("end")
                self.status_var.set(
                    f"✅ Done! Sent: {success}  |  Failed: {failed}")
                messagebox.showinfo("Done!",
                    f"✅ {success} emails sent successfully!" +
                    (f"\n❌ {failed} failed — check the log." if failed else ""))
                self.send_btn.configure(state="normal")

            self.root.after(0, finish)

        threading.Thread(target=do_send, daemon=True).start()


# ================================================================
if __name__ == "__main__":
    root = tk.Tk()
    SalesAutomationApp(root)
    root.mainloop()
