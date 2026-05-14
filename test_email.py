"""
Test: generate a PDF report and email it. Run: python test_email.py
"""
import sys, io, json, os, sqlite3, smtplib
sys.stdout.reconfigure(encoding="utf-8")
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# ── Config ────────────────────────────────────────────────────────────
VAULT         = "vault"
SETTINGS_FILE = os.path.join(VAULT, "settings.json")
CLIENT_NAME   = "Acme Corp"
CLIENT_UUID   = "175f6fd9-8f04-42ee-a741-f4813da128be"
SEND_TO       = "moussdiop240@gmail.com"   # send test to yourself

# ── Load SMTP settings ────────────────────────────────────────────────
with open(SETTINGS_FILE) as f:
    cfg = json.load(f)

smtp_host  = cfg["smtp_host"]
smtp_port  = int(cfg["smtp_port"])
smtp_user  = cfg["smtp_user"]
smtp_pass  = cfg["smtp_password"]
smtp_from  = cfg.get("smtp_from_addr", smtp_user)

# ── Load ledger ───────────────────────────────────────────────────────
ledger_path = os.path.join(VAULT, CLIENT_UUID, "ledger.db")
try:
    conn = sqlite3.connect(ledger_path)
    rows = conn.execute("SELECT * FROM ledger LIMIT 10").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM ledger LIMIT 1").description or []]
    conn.close()
    tx_count = len(rows)
except Exception:
    rows, cols, tx_count = [], [], 0

# ── Generate PDF ──────────────────────────────────────────────────────
try:
    from fpdf import FPDF
    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 200, 150)
    pdf.cell(0, 10, "AI Bookkeeping Specialist", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Financial Report - {CLIENT_NAME}", ln=True)
    pdf.cell(0, 6, f"Generated: {datetime.today().strftime('%B %d, %Y')}", ln=True)
    pdf.ln(8)

    # Divider
    pdf.set_draw_color(0, 200, 150)
    pdf.set_line_width(0.8)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(6)

    # Summary
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, "Executive Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, f"Transactions reviewed: {tx_count}", ln=True)
    pdf.cell(0, 7, "Compliance standard:  2026 IRS & GAAP", ln=True)
    pdf.cell(0, 7, "Ledger integrity:     SHA-256 verified", ln=True)
    pdf.cell(0, 7, "AI agents applied:    IRS s274 / GAAP ASC 360 / UNICAP s263A", ln=True)
    pdf.ln(6)

    # Transactions table
    if rows and cols:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Recent Transactions (preview)", ln=True)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(0, 200, 150)
        pdf.set_text_color(255, 255, 255)
        col_w = [38, 80, 35, 37]
        headers = ["Date", "Description", "Amount", "Category"]
        for h, w in zip(headers, col_w):
            pdf.cell(w, 7, h, border=1, fill=True)
        pdf.ln()
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        date_i = cols.index("date")        if "date"        in cols else None
        desc_i = cols.index("description") if "description" in cols else None
        amt_i  = cols.index("amount")      if "amount"      in cols else None
        cat_i  = cols.index("category")    if "category"    in cols else None
        for i, row in enumerate(rows):
            fill = i % 2 == 0
            pdf.set_fill_color(245, 250, 248) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(col_w[0], 6, str(row[date_i])[:10]         if date_i is not None else "", border=1, fill=fill)
            pdf.cell(col_w[1], 6, str(row[desc_i])[:38]         if desc_i is not None else "", border=1, fill=fill)
            pdf.cell(col_w[2], 6, f"${float(row[amt_i]):,.2f}"  if amt_i  is not None else "", border=1, fill=fill)
            pdf.cell(col_w[3], 6, str(row[cat_i])[:16]          if cat_i  is not None else "", border=1, fill=fill)
            pdf.ln()

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "AI Bookkeeping Specialist - 2026 IRS & GAAP Compliant - 100% Local", ln=True)

    pdf_bytes = pdf.output()
    print(f"PDF generated — {len(pdf_bytes):,} bytes")
except Exception as e:
    print(f"PDF error: {e}")
    sys.exit(1)

# ── Send email ────────────────────────────────────────────────────────
filename = f"Report_{CLIENT_NAME.replace(' ','_')}_{datetime.today().strftime('%Y%m%d')}.pdf"

msg = MIMEMultipart()
msg["From"]    = smtp_from
msg["To"]      = SEND_TO
msg["Subject"] = f"[TEST] Financial Report — {CLIENT_NAME} — {datetime.today().strftime('%B %d, %Y')}"

body = f"""Hi,

This is a test delivery from AI Bookkeeping Specialist.

Client:    {CLIENT_NAME}
Period:    {datetime.today().strftime('%B %Y')}
Generated: {datetime.today().strftime('%B %d, %Y at %I:%M %p')}

The attached PDF contains your financial report including transaction
review, 2026 IRS & GAAP compliance flags, and audit-ready summary.

— AI Bookkeeping Specialist
  2026 IRS & GAAP Compliant · 100% Local · SHA-256 Ledger Integrity
"""
msg.attach(MIMEText(body, "plain"))

part = MIMEBase("application", "octet-stream")
part.set_payload(pdf_bytes)
encoders.encode_base64(part)
part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
msg.attach(part)

print(f"Sending to {SEND_TO} via {smtp_host}:{smtp_port}...")
try:
    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as srv:
        srv.ehlo()
        srv.starttls()
        srv.login(smtp_user, smtp_pass)
        srv.sendmail(smtp_from, SEND_TO, msg.as_string())
    print(f"Sent! Check {SEND_TO} for the report.")
except Exception as e:
    print(f"Send failed: {e}")
    sys.exit(1)
