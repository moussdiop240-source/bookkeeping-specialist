accounting_pipeline/
config/
settings.py        # Application settings and configurations
requirements.txt    # Dependencies required for project execution
data/
local_storage.db   # SQLite database for local data storage and persistence
pi_scrubber/       # Files related to PII scrubbing and anonymization
 RagIndices.csv     # CSV file containing IRS Tax Code (IRC Sections) and US GAAP (FASB ASC Paragraphs)
rag_indices.py     # Python module for creating and managing RAG indices
tax_code/
ira_sections.json  # JSON file containing IRS IRC sections
gaap_framework/
fasc_paragraphs.json    # JSON file containing FASB ASC paragraphs

agentic_debate/
agent_taxes.py       # Module implementing Agent 1 (Tax) optimization logic
agent_gaap.py        # Module implementing Agent 2 (GAAP) optimization logic
reconciler.py        # Module implementing conflict reconciliation and audit logic

reports/
core_statements/     # Folder containing four core statement templates
    balance_sheet.md
    income_statement.md
    cash_flow_statement.md
    statement_of_equity.md

regulations/
gaap_accrual.py      # Module enforcing GAAP accrual principles (ASC 606)
irs_recordkeeping.py # Module implementing IRS recordkeeping and $75 evidence rule
consistency_principle.py  # Module for consistency principle enforcement

ai_advisory/
cash_flow_forecasting.py          # Module providing cash-flow forecasting functionality
current_ratio_analysis.py           # Module providing current-ratio analysis
hash_manager.py                    # Module generating SHA-256 hashes for audit records

utils/
security.py                # Module implementing secure signup/login and password encryption (SHA-256)
ledger_management.py        # Module responsible for creating immutable JSON blocks for audit records

main.py                      # Entry point of the application, orchestrating phases
__init__.py                   # Initialization module ensuring proper installation and execution
