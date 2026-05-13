"""Generate AI Bookkeeping Specialist documentation PDF from README.md content."""
from fpdf import FPDF
from datetime import datetime
import os

OUT = os.path.join(os.path.dirname(__file__), "AI_Bookkeeping_Specialist_Docs.pdf")

class DocPDF(FPDF):
    def header(self):
        self.set_fill_color(8, 13, 24)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(0, 200, 150)
        self.set_y(4)
        self.cell(0, 6, "AI Bookkeeping Specialist  |  2026 Edition", align="L")
        self.set_text_color(84, 104, 128)
        self.cell(0, 6, f"Generated {datetime.today().strftime('%B %d, %Y')}", align="R")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_fill_color(8, 13, 24)
        self.rect(0, self.get_y(), 210, 12, "F")
        self.set_font("Helvetica", "", 7)
        self.set_text_color(84, 104, 128)
        self.cell(0, 8, f"Page {self.page_no()}  |  2026 IRS & GAAP Compliant  |  100% Local  |  SHA-256 Ledger Integrity", align="C")

def cover(pdf):
    pdf.add_page()
    # Dark cover background
    pdf.set_fill_color(8, 13, 24)
    pdf.rect(0, 0, 210, 297, "F")

    # Accent bar
    pdf.set_fill_color(0, 200, 150)
    pdf.rect(0, 110, 210, 3, "F")

    # Title
    pdf.set_y(60)
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_text_color(240, 244, 250)
    pdf.cell(0, 14, "AI Bookkeeping Specialist", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(0, 200, 150)
    pdf.cell(0, 10, "2026 Edition  |  User & Value Guide", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(138, 155, 181)
    pdf.cell(0, 7, "Audit-Ready Financials.  Zero Cloud Risk.  Built for CPAs.", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(180)
    for line in [
        "  2026 IRS & GAAP Compliant",
        "  SHA-256 Ledger Integrity",
        "  100% Local - No Cloud Sync",
        "  IRS $75 Safe-Harbor Built In",
    ]:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(84, 104, 128)
        pdf.cell(0, 8, line, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(250)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(0, 200, 150)
    pdf.cell(0, 7, "$299 Setup  |  $49.99/mo  |  14-Day Free Trial", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(84, 104, 128)
    pdf.cell(0, 6, "moustaphaleye.diop@gmail.com", align="C")

def section_header(pdf, title):
    pdf.ln(4)
    pdf.set_fill_color(0, 30, 20)
    pdf.set_text_color(0, 200, 150)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_text_color(30, 30, 40)
    pdf.ln(2)

def h2(pdf, title):
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 112, 243)
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(40, 40, 50)
    pdf.ln(1)

def body(pdf, text, indent=0):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 55, 65)
    pdf.set_x(10 + indent)
    pdf.multi_cell(190 - indent, 5.5, text)
    pdf.ln(1)

def bullet(pdf, text, indent=4):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 55, 65)
    pdf.set_x(10 + indent)
    pdf.cell(4, 5.5, chr(149))
    pdf.set_x(16 + indent)
    pdf.multi_cell(184 - indent, 5.5, text)

def table_row(pdf, cols, widths, header=False, shade=False):
    row_h = 6
    if pdf.get_y() + row_h > pdf.h - pdf.b_margin:
        pdf.add_page()
    if shade:
        pdf.set_fill_color(245, 248, 252)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.set_font("Helvetica", "B" if header else "", 8)
    pdf.set_text_color(30, 30, 40) if not header else pdf.set_text_color(255, 255, 255)
    if header:
        pdf.set_fill_color(8, 13, 24)
    x = pdf.get_x()
    y = pdf.get_y()
    pdf.set_auto_page_break(False)
    for col, w in zip(cols, widths):
        pdf.set_xy(x, y)
        pdf.cell(w, row_h, col, border=1, fill=True)
        x += w
    pdf.set_auto_page_break(True, margin=16)
    pdf.ln(row_h)

def divider(pdf):
    pdf.set_draw_color(220, 228, 235)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

def callout(pdf, text, color=(0, 200, 150)):
    pdf.set_fill_color(8, 30, 22)
    pdf.set_text_color(*color)
    pdf.set_font("Helvetica", "BI", 9)
    pdf.set_x(10)
    pdf.multi_cell(190, 6, f"  {text}", fill=True)
    pdf.set_text_color(50, 55, 65)
    pdf.ln(2)

# ── BUILD PDF ─────────────────────────────────────────────────────────────────
pdf = DocPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=16)
pdf.set_margins(10, 16, 10)

cover(pdf)

# ── SECTION 1: WHY USE THIS APP ───────────────────────────────────────────────
pdf.add_page()
section_header(pdf, "SECTION 1 - WHY USE THIS APP")
h2(pdf, "The Value Proposition for Small Business Owners")

body(pdf, "Most small business owners do one of three things with their bookkeeping:")
for b in [
    "Pay a CPA $200-$400/hour to review transactions after the fact",
    "Use QuickBooks Online ($30-$200/month) and hope the automated categorization is right",
    "Ignore it until tax season -- then panic",
]:
    bullet(pdf, b)

pdf.ln(3)
body(pdf, "All three share the same problem: nobody is checking whether your expenses will survive an IRS audit until it is too late. The IRS does not care that you forgot a receipt. They care about the rules -- and the rules are specific.")

pdf.ln(2)
h2(pdf, "What Non-Compliance Actually Costs")

headers = ["Situation", "What Happens"]
widths  = [95, 95]
table_row(pdf, headers, widths, header=True)
rows = [
    ("$300 business dinner, no receipt", "IRS disallows under Sec. 274. Taxes + penalties + interest."),
    ("$5,000 laptop expensed in full",   "GAAP requires capitalization. P&L overstated."),
    ("Product business, no UNICAP",      "Under-reported inventory costs. Sec. 263A adjustment owed."),
    ("100% meals deduction",             "Legal limit is 50%. Deductions overstated every year."),
]
for i, (a, b) in enumerate(rows):
    table_row(pdf, [a, b], widths, shade=(i % 2 == 0))
pdf.ln(3)

body(pdf, "These are not edge cases. They are the four most common audit triggers for Schedule C filers -- and they happen to businesses that are doing everything else right.")

pdf.ln(2)
h2(pdf, "How AI Bookkeeping Specialist Fixes This")
body(pdf, "Every transaction you import gets reviewed by three AI agents simultaneously:")
for b in [
    "IRS Agent -- checks the $75 receipt threshold and Sec. 274 substantiation requirements on every line item",
    "GAAP Agent -- flags expenses over $2,000 that should be capitalized as assets instead of expensed",
    "UNICAP Agent -- identifies inventory and production costs subject to Sec. 263A uniform capitalization",
]:
    bullet(pdf, b)

pdf.ln(3)
body(pdf, "You get a plain-English verdict on every transaction: Cleared, Flagged, or Capitalize? -- with the exact IRS code cited. Not a vague warning. The actual rule.")

pdf.ln(2)
callout(pdf, "You stop finding out about problems when the IRS letter arrives. You find out on Tuesday morning, when you import your bank statement -- before the return is filed, before penalties accrue.")

pdf.ln(2)
h2(pdf, "It Runs on Your Machine. Not Ours.")
body(pdf, "Your financial data never leaves your computer. No cloud sync. No monthly SaaS subscription per client. No vendor with access to your books. SHA-256 hashing makes the ledger tamper-evident. The AI model runs locally via Ollama.")

pdf.ln(2)
callout(pdf, "The Bottom Line: A one-time $299 setup covers the cost of catching a single disallowed deduction that would have triggered an IRS notice. Every year after that costs less than one hour of CPA time.")

divider(pdf)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(0, 200, 150)
body(pdf, "Pricing:  $299 one-time setup  |  $49.99/month  |  14-day free trial, no credit card required")

# ── SECTION 2: HOW TO USE THE AI TAX AUDITOR ─────────────────────────────────
pdf.add_page()
section_header(pdf, "SECTION 2 - HOW TO USE THE AI TAX AUDITOR")

h2(pdf, "What It Is")
body(pdf, "The AI Tax Auditor (called Agentic Debate in the pipeline) runs three independent compliance agents against every transaction in your active client's ledger. Each agent applies a different standard and works in parallel -- no agent can override another.")
body(pdf, "Navigate to it via the sidebar:  Agentic Debate")

pdf.ln(2)
h2(pdf, "Before You Start")
bullet(pdf, "A client loaded -- click Client Management, select a client, click Load Client")
bullet(pdf, "Ledger data imported -- at least one transaction via Ingestion or AI Categorization")
pdf.ln(1)
body(pdf, "If the ledger is empty, the auditor shows an info message. Import data first.")

pdf.ln(2)
h2(pdf, "Running the Audit")
body(pdf, "Navigate to Agentic Debate. The audit runs automatically on page load -- no button to click. Every transaction in the ledger is processed immediately.")

pdf.ln(2)
h2(pdf, "Reading the Verdict Cards")

headers = ["Badge", "Meaning"]
widths  = [35, 155]
table_row(pdf, headers, widths, header=True)
badges = [
    ("CLEARED",     "Transaction passes this agent's standard. No action needed."),
    ("FLAGGED",     "Transaction fails or is at risk. Action required before filing."),
    ("CAPITALIZE?", "Transaction may need to be recorded as an asset, not an expense."),
    ("ADJUST",      "UNICAP uniform capitalization adjustment estimated."),
]
for i, (a, b) in enumerate(badges):
    table_row(pdf, [a, b], widths, shade=(i % 2 == 0))
pdf.ln(3)

body(pdf, "Each card also shows a Confidence Score (how certain the agent is -- low score means get professional review) and an Action Line (the exact step to take, with IRS/GAAP code cited).")

pdf.ln(3)
h2(pdf, "Agent 1 -- IRS Section 274: Receipt Substantiation")
body(pdf, "Applies the receipt rules under IRC Section 274.")

headers = ["Amount", "Verdict", "What It Means"]
widths  = [45, 40, 105]
table_row(pdf, headers, widths, header=True)
rows274 = [
    ("$75 or less",      "CLEARED",          "IRS safe harbor -- no receipt required"),
    ("$76 to $500",      "FLAGGED (medium)",  "Receipt + written business purpose required"),
    ("$501 to $1,000",   "FLAGGED (high)",    "Elevated audit probability -- document now"),
    ("Over $1,000",      "FLAGGED (critical)","Priority documentation -- do not file without receipt"),
]
for i, r in enumerate(rows274):
    table_row(pdf, list(r), widths, shade=(i % 2 == 0))
pdf.ln(2)
bullet(pdf, "What to do when flagged: Locate the receipt. If missing, reconstruct the business purpose in writing -- note the date, amount, attendees, and business reason. Keep with your records.")

pdf.ln(3)
h2(pdf, "Agent 2 -- GAAP ASC 360: Capitalization Threshold")
body(pdf, "Applies the capitalization rules under ASC 360 (Property, Plant & Equipment).")

headers = ["Amount", "Verdict", "What It Means"]
table_row(pdf, headers, widths, header=True)
rows360 = [
    ("$2,000 or less",    "EXPENSED",           "Standard period cost -- expense as incurred"),
    ("$2,001 to $10,000", "CAPITALIZE? (medium)","Review useful life -- may need to be an asset"),
    ("Over $10,000",      "CAPITALIZE? (high)",  "Almost certainly requires capitalization"),
]
for i, r in enumerate(rows360):
    table_row(pdf, list(r), widths, shade=(i % 2 == 0))
pdf.ln(2)
bullet(pdf, "What to do when flagged: Ask whether this item has a useful life greater than one year. A laptop, piece of equipment, or vehicle must be capitalized and depreciated, not expensed in full. Move it to your asset schedule.")

pdf.ln(3)
h2(pdf, "Agent 3 -- UNICAP Section 263A: Uniform Capitalization")
body(pdf, "Only triggers on inventory, production, manufacturing, COGS, materials, resale, freight, or packaging categories. Estimates a 10% capitalization adjustment on qualifying costs over $1,000.")
bullet(pdf, "What to do when flagged: Review whether these costs relate to goods held for sale. If yes, a portion must be added to inventory cost rather than expensed immediately. Your CPA calculates the exact Sec. 263A adjustment at year-end.")

pdf.ln(3)
h2(pdf, "The Final Verdict")

headers = ["Risk Level", "Meaning"]
widths  = [45, 145]
table_row(pdf, headers, widths, header=True)
risk_rows = [
    ("Low Risk",    "Fewer than 10% of transactions flagged"),
    ("Medium Risk", "10 to 30% flagged, or high-value flags present"),
    ("High Risk",   "Over 30% flagged, or critical flags present"),
]
for i, r in enumerate(risk_rows):
    table_row(pdf, list(r), widths, shade=(i % 2 == 0))
pdf.ln(2)
body(pdf, "Use this as your client briefing headline: \"Your ledger is Medium Risk -- 4 transactions need receipts and 1 needs to be reclassified as an asset.\"")

pdf.ln(3)
h2(pdf, "Exporting the Results")
body(pdf, "Click Export Debate Results at the bottom of the page. Downloads a CSV with every transaction, each agent verdict, confidence score, and action line.")
for b in [
    "Attach to the client audit file",
    "Email to your CPA alongside the PDF report",
    "Keep as year-end documentation in case of IRS correspondence",
]:
    bullet(pdf, b)

pdf.ln(3)
h2(pdf, "Common Questions")
faqs = [
    ("A transaction is flagged but I have the receipt -- what do I do?",
     "Having the receipt means you are protected. The flag is a reminder to document, not a finding that you did something wrong. Keep the receipt with your records."),
    ("The confidence score is 40% -- should I worry?",
     "Low confidence means the agent is uncertain -- typically because the amount is close to a threshold or the category is ambiguous. Get a second opinion from your CPA on those items."),
    ("All my transactions are under $75 but I am still flagged.",
     "Check the GAAP and UNICAP agents -- the $75 threshold only applies to IRS Section 274. A $60 purchase categorized as inventory will still trigger the UNICAP agent."),
    ("Can I clear a flag inside the app?",
     "Not currently. Re-categorize the transaction in AI Categorization, then return to Agentic Debate -- the agents re-run on the updated data automatically."),
]
for q, a in faqs:
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(0, 112, 243)
    pdf.set_x(10)
    pdf.multi_cell(190, 5.5, q)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 55, 65)
    pdf.set_x(14)
    pdf.multi_cell(186, 5.5, a)
    pdf.ln(2)

# ── SYSTEM REQUIREMENTS ───────────────────────────────────────────────────────
pdf.ln(2)
divider(pdf)
h2(pdf, "System Requirements")
headers = ["Requirement", "Minimum"]
widths  = [60, 130]
table_row(pdf, headers, widths, header=True)
reqs = [
    ("OS",        "Windows 10 or later"),
    ("Python",    "3.11+"),
    ("RAM",       "4 GB (8 GB recommended for Ollama)"),
    ("Storage",   "2 GB free (for the AI model)"),
    ("Ollama",    "Latest stable release from ollama.ai"),
    ("AI Model",  "llama3.2:1b (auto-downloaded by launch.bat)"),
]
for i, r in enumerate(reqs):
    table_row(pdf, list(r), widths, shade=(i % 2 == 0))

pdf.ln(4)
divider(pdf)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(0, 200, 150)
body(pdf, "License: $299 setup fee / $49.99/month / 14-day free trial  |  Contact: moustaphaleye.diop@gmail.com")

pdf.output(OUT)
print(f"PDF saved: {OUT}")
