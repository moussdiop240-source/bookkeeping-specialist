"""
Standalone test for Receipt Vault pure functions.
Run with: python test_receipt_vault.py
"""
import io, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd
from datetime import datetime

# ── Copy of the pure functions (no Streamlit dependency) ─────────────

def _parse_receipt_text(text: str) -> dict:
    amt_candidates = re.findall(r'\$?\s*(\d{1,6}[.,]\d{2})\b', text)
    amount = None
    if amt_candidates:
        try:
            amounts = [float(a.replace(",", "")) for a in amt_candidates]
            amount = max(amounts)
        except ValueError:
            pass

    date_str = None
    date_patterns = [
        r'\b(\d{4}-\d{2}-\d{2})\b',
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b',
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2})\b',
        r'\b([A-Za-z]{3,9}\.?\s+\d{1,2},?\s+\d{4})\b',
    ]
    fmt_sets = [
        ["%Y-%m-%d"],
        ["%m/%d/%Y", "%m-%d-%Y"],
        ["%m/%d/%y", "%m-%d-%y"],
        ["%B %d, %Y", "%B %d %Y", "%b %d, %Y", "%b %d %Y"],
    ]
    for pat, fmts in zip(date_patterns, fmt_sets):
        m = re.search(pat, text)
        if m:
            raw = m.group(1).strip().rstrip(",")
            for fmt in fmts:
                try:
                    date_str = datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
        if date_str:
            break

    vendor = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and len(stripped) > 2 and not re.match(r'^[\d\s$.,/-]+$', stripped):
            vendor = stripped[:60]
            break

    return {"vendor": vendor, "amount": amount, "date": date_str}


def _match_receipts_to_ledger(ledger_df, receipts_df):
    result = ledger_df.copy()
    result["receipt_status"] = "Missing Receipt ⚠️"
    result["matched_vendor"]  = ""

    if receipts_df.empty or "amount" not in receipts_df.columns:
        return result

    result["_tx_date"] = pd.to_datetime(result.get("date", pd.Series(dtype=str)), errors="coerce")
    rec = receipts_df.copy()
    rec["_r_date"] = pd.to_datetime(rec.get("date", pd.Series(dtype=str)), errors="coerce")
    rec_valid = rec.dropna(subset=["_r_date", "amount"])

    for idx, tx in result.iterrows():
        tx_date   = tx["_tx_date"]
        tx_amount = float(tx.get("amount") or 0)
        if pd.isna(tx_date):
            continue
        for _, rr in rec_valid.iterrows():
            date_diff   = abs((tx_date - rr["_r_date"]).days)
            amount_diff = abs(tx_amount - float(rr["amount"] or 0))
            if date_diff <= 2 and amount_diff <= 0.01:
                result.at[idx, "receipt_status"] = "Verified ✅"
                result.at[idx, "matched_vendor"]  = rr.get("vendor", "")
                break

    result.drop(columns=["_tx_date"], inplace=True)
    return result


# ── Test runner ───────────────────────────────────────────────────────

passed = failed = 0

def check(label, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  ✅ PASS  {label}")
        passed += 1
    else:
        print(f"  ❌ FAIL  {label}{(' — ' + detail) if detail else ''}")
        failed += 1

print("=" * 62)
print("RECEIPT VAULT — TEST SUITE")
print("=" * 62)

# ── TEST 1: OCR text parser ───────────────────────────────────────────
print("\nTEST 1: _parse_receipt_text")

r = _parse_receipt_text(
    "Home Depot\n1234 Main St\n05/10/2026\n"
    "Screws  $4.99\nPaint  $22.50\nTOTAL  $27.49"
)
check("vendor extracted",        r["vendor"] == "Home Depot",    repr(r["vendor"]))
check("amount = largest figure", r["amount"] == 27.49,           repr(r["amount"]))
check("date MM/DD/YYYY",         r["date"]   == "2026-05-10",    repr(r["date"]))

r = _parse_receipt_text("AMAZON.COM\nOrder 2026-05-08\nOffice Chair\nTotal: $349.00")
check("ISO date",   r["date"]   == "2026-05-08", repr(r["date"]))
check("ISO amount", r["amount"] == 349.00,        repr(r["amount"]))

r = _parse_receipt_text(
    "STARBUCKS #4421\nMay 12, 2026\nLatte $6.75\nTip $1.25\nTotal $8.00"
)
check("long-form date",  r["date"]   == "2026-05-12", repr(r["date"]))
check("max amount wins", r["amount"] == 8.00,          repr(r["amount"]))

r = _parse_receipt_text("DELTA AIRLINES\n04-22-2026\nFlight LAX-JFK\n$512.00")
check("dash-separated date", r["date"] == "2026-04-22", repr(r["date"]))

r = _parse_receipt_text("")
check("empty text → no crash", r["amount"] is None and r["date"] is None)

# ── TEST 2: Matching engine ───────────────────────────────────────────
print("\nTEST 2: _match_receipts_to_ledger")

ledger = pd.DataFrame([
    {"date": "2026-05-10", "description": "Home Depot",    "amount": 27.49,  "category": "Supplies"},
    {"date": "2026-05-08", "description": "Amazon",        "amount": 349.00, "category": "Equipment"},
    {"date": "2026-05-12", "description": "Starbucks",     "amount": 8.00,   "category": "Meals"},
    {"date": "2026-05-01", "description": "Unmatched Exp", "amount": 150.00, "category": "Travel"},
])
receipts = pd.DataFrame([
    {"vendor": "Home Depot",      "amount": 27.49,  "date": "2026-05-10"},
    {"vendor": "Amazon.com",      "amount": 349.00, "date": "2026-05-09"},
    {"vendor": "Starbucks #4421", "amount": 8.00,   "date": "2026-05-14"},
])

result = _match_receipts_to_ledger(ledger, receipts)
check("exact match → Verified",       result.at[0, "receipt_status"] == "Verified ✅")
check("1-day window → Verified",      result.at[1, "receipt_status"] == "Verified ✅")
check("2-day window → Verified",      result.at[2, "receipt_status"] == "Verified ✅")
check("no receipt → Missing Receipt", result.at[3, "receipt_status"] == "Missing Receipt ⚠️")
check("vendor name propagated",       result.at[0, "matched_vendor"] == "Home Depot")

# Edge: 3-day gap must NOT match
l2 = pd.DataFrame([{"date": "2026-05-10", "description": "X", "amount": 50.00, "category": ""}])
r2 = pd.DataFrame([{"vendor": "X", "amount": 50.00, "date": "2026-05-07"}])
check("3-day gap → Missing Receipt",
      _match_receipts_to_ledger(l2, r2).at[0, "receipt_status"] == "Missing Receipt ⚠️")

# Edge: $0.02 amount gap must NOT match
l3 = pd.DataFrame([{"date": "2026-05-10", "description": "X", "amount": 27.51, "category": ""}])
r3 = pd.DataFrame([{"vendor": "X", "amount": 27.49, "date": "2026-05-10"}])
check("$0.02 gap → Missing Receipt",
      _match_receipts_to_ledger(l3, r3).at[0, "receipt_status"] == "Missing Receipt ⚠️")

# Edge: empty receipts
check("empty receipts df → all Missing",
      (_match_receipts_to_ledger(ledger, pd.DataFrame())["receipt_status"]
       == "Missing Receipt ⚠️").all())

# ── TEST 3: pdfplumber ────────────────────────────────────────────────
print("\nTEST 3: pdfplumber PDF extraction")
try:
    import pdfplumber
    # Build a minimal in-memory PDF using fpdf2
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 10, "ACME SUPPLIES", ln=True)
        pdf.cell(0, 10, "Date: 2026-05-10", ln=True)
        pdf.cell(0, 10, "Widget x3   $45.00", ln=True)
        pdf.cell(0, 10, "TOTAL       $45.00", ln=True)
        pdf_bytes = pdf.output()

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
            text = "\n".join(p.extract_text() or "" for p in pdf_doc.pages)
        parsed = _parse_receipt_text(text)
        check("PDF vendor extracted", "ACME" in parsed.get("vendor",""), repr(parsed["vendor"]))
        check("PDF amount extracted", parsed["amount"] == 45.00,         repr(parsed["amount"]))
        check("PDF date extracted",   parsed["date"] == "2026-05-10",    repr(parsed["date"]))
    except ImportError:
        print("  ⚠️  fpdf2 not available for synthetic PDF — skipping PDF content test")
        print(f"  ✅ PASS  pdfplumber {pdfplumber.__version__} importable")
except ImportError as e:
    check("pdfplumber importable", False, str(e))

# ── TEST 4: pytesseract ───────────────────────────────────────────────
print("\nTEST 4: pytesseract / Tesseract binary")
try:
    import pytesseract, os
    _tess = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(_tess):
        pytesseract.pytesseract.tesseract_cmd = _tess
    ver = pytesseract.get_tesseract_version()
    check(f"Tesseract binary found ({ver})", True)
except Exception as e:
    print(f"  ⚠️  WARN  Tesseract binary not installed — image OCR disabled")
    print(f"           PDF OCR (pdfplumber) is fully operational.")
    print(f"           Install from: https://github.com/UB-Mannheim/tesseract/wiki")

# ── Summary ───────────────────────────────────────────────────────────
print()
print("=" * 62)
total = passed + failed
print(f"RESULT: {passed}/{total} passed", end="  ")
print("✅ ALL PASSED" if failed == 0 else f"❌ {failed} FAILED")
print("=" * 62)
