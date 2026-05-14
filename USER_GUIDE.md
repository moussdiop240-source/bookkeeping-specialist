# AI Bookkeeping Specialist — User Guide
### 2026 IRS & GAAP Edition

---

## Why Use This App

Most bookkeeping tools tell you what happened. This app tells you whether what happened will survive an IRS audit.

Every transaction you import is reviewed by three independent AI agents — one for IRS receipt substantiation rules (§274), one for GAAP capitalization thresholds (ASC 360), and one for inventory cost allocation (UNICAP §263A). You get a plain-English verdict on every line item before you file, not after.

The app runs entirely on your machine. Your financial data never touches a server. The AI model (Llama 3.2) runs locally via Ollama. SHA-256 hashing makes the ledger tamper-evident.

---

## How It Works

### The Pipeline — 14 Phases

Work left to right through the sidebar:

| Phase | What It Does |
|---|---|
| 🏠 Command Center | Portfolio overview across all clients — revenue, flags, compliance score |
| 🏢 Client Management | Create, load, backup, and restore client vaults |
| 💳 Subscription | Activate or renew your license key; pay via Stripe |
| 📥 Ingestion | Import bank statements (CSV, Excel, OFX, QFX) with auto dedup |
| 💰 Revenue | Log revenue entries per client |
| 🏷️ AI Categorization | One-click GAAP category assignment via local AI |
| 🤖 Agentic Debate | Three-agent IRS/GAAP/UNICAP compliance review |
| 📊 Financial Reporting | P&L summary with burn rate trend |
| 📑 Financial Statements | Balance sheet and income statement view |
| 📈 CFO Dashboard | High-level KPI cards and charts |
| 📄 PDF Reports | Generate and download a 7-section audit-ready PDF |
| 📋 Tax Readiness | Schedule C/E worksheet generator, UNICAP calculator, year-end checklist |
| 🧾 Receipt Vault | Upload receipts → OCR extracts fields → matches against ledger |
| 📧 Email Delivery | Send PDF reports directly to clients via SMTP |
| 💬 AI CFO Chat | Conversational AI for financial questions about the active client |

---

### First-Run Sequence

```
1. Open Client Management → Create a client workspace
2. Click Load Client to make it active
3. Go to Subscription → enter your license key to activate
4. Go to Ingestion → upload a bank statement CSV or OFX file
5. Go to AI Categorization → run auto-categorization
6. Go to Agentic Debate → review compliance verdicts
7. Go to PDF Reports → generate and download the report
```

---

### How the Agentic Debate Works

Three agents run against every transaction simultaneously:

**IRS §274 Agent — Receipt Substantiation**
- Transactions ≤ $75: CLEARED (safe harbor, no receipt required)
- $76–$500: FLAGGED (receipt + written business purpose required)
- $501–$1,000: FLAGGED HIGH (elevated audit probability)
- Over $1,000: FLAGGED CRITICAL (document immediately)

**GAAP ASC 360 Agent — Capitalization**
- ≤ $2,000: EXPENSED (standard period cost)
- $2,001–$10,000: CAPITALIZE? (review useful life)
- Over $10,000: CAPITALIZE HIGH (almost certainly an asset, not an expense)

**UNICAP §263A Agent — Inventory Cost Allocation**
- Only triggers on inventory, production, COGS, freight, packaging categories
- Flags amounts over $1,000 in qualifying categories for uniform capitalization review

Every debate run is automatically saved to the client's ledger database. You can also export results as CSV.

---

### How the Receipt Vault Works

1. Navigate to 🧾 Receipt Vault (or drop a file in the sidebar quick-uploader)
2. Upload one or more PDF or image receipts
3. The OCR engine extracts Vendor, Amount, and Date from each file
4. Review and correct the extracted fields if needed
5. Save receipts to the vault
6. The Matching Engine compares each stored receipt against the ledger:
   - Amount must match within $0.01
   - Date must be within ±2 calendar days
7. The Audit Log table shows every transaction tagged Verified ✅ or Missing Receipt ⚠️
8. Export the audit log as CSV for your CPA

**Dependencies required:**
```
pip install pdfplumber      # PDF text extraction
pip install pytesseract     # image OCR
```
For image OCR on Windows, also install the Tesseract binary:
https://github.com/UB-Mannheim/tesseract/wiki

---

## Troubleshooting Local Ollama Connections

The app uses the Llama 3.2 model running locally via Ollama. If the AI features are not working, work through these steps in order.

---

### Step 1 — Confirm Ollama Is Running

Open a terminal and run:
```
ollama list
```
If you get a connection error, Ollama is not running. Start it:
```
ollama serve
```
Leave that terminal open. The app connects to `http://localhost:11434`.

---

### Step 2 — Confirm the Model Is Installed

```
ollama list
```
You should see `llama3.2:1b` in the output. If not, pull it:
```
ollama pull llama3.2:1b
```
This downloads approximately 1.3 GB. Wait for it to complete before using AI features.

---

### Step 3 — Check the Sidebar Status Indicator

The sidebar shows the Ollama status in real time:
- 🟢 **Online** — model ready, AI features fully operational
- 🟡 **Warming** — model is loading (wait 30–60 seconds and refresh)
- 🔴 **Offline** — Ollama is not reachable (go back to Step 1)

---

### Step 4 — Test the Connection Manually

In a terminal:
```
curl http://localhost:11434/api/tags
```
Expected output: a JSON object listing installed models. If you get "connection refused", Ollama is not running.

---

### Step 5 — Firewall and Port Conflicts

If Ollama is running but the app cannot connect:

1. Check if port 11434 is blocked by your firewall — add an inbound rule for TCP 11434
2. Check if another process is using the port:
   ```
   netstat -ano | findstr :11434
   ```
3. If the port is in use by another process, restart Ollama after killing that process

---

### Step 6 — Slow or Hanging AI Responses

The local model may be slow on machines with less than 8 GB RAM or no GPU. Symptoms: categorization takes 30+ seconds per transaction, or the chat hangs.

Options:
- Use AI Categorization in small batches (import fewer rows at a time)
- Close other applications to free RAM
- The AI CFO Chat has a 30-second timeout — if the model is cold, click Send again after it loads

---

### Step 7 — AI Categorization Returns "Uncategorized"

This means the model responded but returned an unexpected format. Try:
1. Go to AI Categorization → re-run on the affected rows
2. If it persists, check Ollama logs in the terminal where `ollama serve` is running
3. Manually assign a category by re-importing with a pre-categorized CSV

---

### Common Error Messages

| Message | Cause | Fix |
|---|---|---|
| `Connection refused` | Ollama not running | Run `ollama serve` |
| `model not found` | llama3.2:1b not installed | Run `ollama pull llama3.2:1b` |
| `timeout` | Model still loading | Wait 30–60s, try again |
| `No ledger data found` | No client loaded or no import done | Load a client, then import via Ingestion |
| `Invalid license key` | Wrong key format or wrong client | Check key type: SETUP keys activate, RENEW keys extend |
| `pdfplumber not installed` | Missing dependency | Run `pip install pdfplumber` |
| `pytesseract not installed` | Missing dependency | Run `pip install pytesseract` + install Tesseract binary |

---

## License & Support

- Setup: $299 one-time
- Monthly renewal: $49.99/month
- Trial: 14 days, full access, no credit card required

Contact: moustaphaleye.diop@gmail.com

2026 IRS & GAAP Compliant · SHA-256 Ledger Integrity · 100% Local
