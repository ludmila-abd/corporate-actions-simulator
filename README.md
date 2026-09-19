# Corporate Actions Processing Engine

## Portfolio Impact, Exception Management, Audit Trail and Streamlit Control Dashboard

This project simulates how a **Corporate Actions / Asset Services** team processes stock splits, cash dividends and spin-offs across a portfolio.

The goal is not just to update holdings.

The goal is to process valid corporate actions automatically, reject bad records before they affect the portfolio, preserve cost basis, update cash correctly, and produce a full audit trail.

This project includes:

1. A Python notebook processing engine
2. A reporting-ready Excel export
3. An interactive Streamlit control dashboard
4. Audit, reconciliation and exception-management outputs

---

## Project Summary

Corporate actions can materially affect client portfolios.

When a company announces a split, dividend or spin-off, an operations team must ensure that:

- eligible accounts are correctly identified
- share quantities are updated accurately
- cash movements are calculated correctly
- cost basis is preserved where required
- invalid events are stopped before processing
- exceptions are reviewed before they reach client reporting

This project builds a simplified but realistic version of that workflow.

The engine processes a mock corporate actions feed containing both valid and deliberately broken records.

---

## Core Question

> Can we process a corporate actions feed automatically while catching bad data before it corrupts the portfolio?

---

## What the Project Does

The simulator starts with a sample equity portfolio containing:

- AAPL
- MSFT
- KO
- GE

It then processes five corporate actions:

| Event | Type | Expected Outcome |
|---|---|---|
| AAPL 4-for-1 split | Stock split | Valid - shares increase and average cost falls |
| KO cash dividend | Cash dividend | Valid - cash ledger increases |
| GE spin-off into GEV | Spin-off | Valid - new GEV position is created |
| MSFT split with negative ratio | Broken split | Invalid - routed to exception queue |
| TSLA dividend | Ineligible dividend | Invalid - ticker not held in portfolio |

---

## Key Control Principle

A valid corporate action should not arbitrarily create or destroy accounting value.

For stock splits and spin-offs, the main validation rule is:

    Cost basis before ≈ Cost basis after

The portfolio may change shape, but the economic cost basis should reconcile.

This project checks that principle after every processed event.

---

## Project Architecture

    Corporate Actions Feed
            ↓
    Validation Engine
            ↓
    Processing Engine
            ↓
    Position Book Update
            ↓
    Cash Ledger Update
            ↓
    Audit Log
            ↓
    Exception Queue
            ↓
    Reconciliation Controls
            ↓
    Excel Export + Streamlit Dashboard

---

## Project Structure

    corporate-actions-simulator/
    │
    ├── Corporate_Actions_Impact_Simulator.ipynb
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    │
    ├── .streamlit/
    │   └── config.toml
    │
    └── outputs/
        ├── corporate_actions_powerbi_export.xlsx
        ├── corp_actions_cost_basis_before_after.png
        ├── corp_actions_shares_before_after.png
        ├── corp_actions_processing_status.png
        ├── corp_actions_kpi_dashboard.png
        └── corp_actions_exception_reason_codes.png

---

## Notebook Sections

The notebook is structured as a complete processing workflow:

1. Executive introduction
2. Setup and project configuration
3. Starting portfolio / position book
4. Corporate actions feed / event queue
5. Validation engine
6. Processing engine
7. Queue processing workflow
8. Audit log, exception queue and cash ledger
9. Final portfolio and reconciliation controls
10. Visual dashboard
11. Exception severity and SLA review
12. Excel / reporting export package

---

## Starting Portfolio

The starting portfolio contains four holdings:

| Ticker | Company | Corporate Action Exposure |
|---|---|---|
| AAPL | Apple Inc. | Stock split |
| MSFT | Microsoft Corp. | Broken split action |
| KO | The Coca-Cola Company | Cash dividend |
| GE | General Electric | Spin-off into GEV |

The initial portfolio has a total cost basis of:

    $286,000

This is the baseline used for reconciliation.

---

## Corporate Actions Feed

The project uses a mock vendor feed with five events.

Three are valid:

- AAPL stock split
- KO cash dividend
- GE spin-off

Two are intentionally invalid:

- MSFT split with a negative ratio
- TSLA dividend for a ticker not held in the portfolio

The broken events are included on purpose to prove that the validation layer works.

---

## Validation Engine

Before processing any event, the validation engine checks:

| Rule | Purpose |
|---|---|
| Action type is supported | Prevents unknown event types |
| Ticker exists in portfolio | Prevents ineligible events |
| Position is eligible | Confirms event can apply to the account |
| Split ratio is positive | Prevents impossible quantity updates |
| Dividend amount is positive | Prevents invalid cash movements |
| Spin-off fields are complete | Ensures child security can be created |
| Cost-basis allocations sum to 100% | Prevents basis breaks |
| Ex-date is not after payable date | Catches date-sequencing errors |

Invalid events are not processed.

They are routed to the exception queue.

---

## Processing Engine

The processing engine contains separate logic for each event type.

### Stock Split

For a valid split:

- shares increase by the split ratio
- average cost decreases by the split ratio
- market price adjusts by the split ratio
- total cost basis remains unchanged

Example:

    AAPL 4-for-1 split
    500 shares → 2,000 shares
    $150 average cost → $37.50 average cost
    Cost basis remains $75,000

---

### Cash Dividend

For a valid dividend:

- share quantity is unchanged
- average cost is unchanged
- cost basis is unchanged
- cash ledger increases

Example:

    KO dividend
    1,000 shares × $0.485 = $485 cash generated

---

### Spin-Off

For a spin-off:

- parent shares remain
- child shares are created
- original cost basis is allocated between parent and child

Example:

    GE spin-off into GEV
    GE remains in the portfolio
    New GEV position is created
    Total GE + GEV cost basis remains unchanged

---

## Processing Results

The engine processed the five events as follows:

| Metric | Result |
|---|---:|
| Events received | 5 |
| Events processed | 3 |
| Events flagged | 2 |
| Straight-through processing rate | 60% |
| Exception rate | 40% |
| Cash generated | $485 |
| Cost basis difference | $0 |

The final reconciliation passed.

---

## Exception Management

Two events were flagged for manual review.

| Ticker | Event Type | Reason |
|---|---|---|
| MSFT | Split | Invalid split ratio |
| TSLA | Cash dividend | Ticker not held in portfolio |

The enriched exception queue adds:

- reason code
- severity
- SLA status
- review owner
- required action

This makes the exception queue supervisor-ready.

---

## Reconciliation Controls

The reconciliation layer checks:

| Control | Result |
|---|---|
| Total cost basis before | $286,000 |
| Total cost basis after | $286,000 |
| Cost basis difference | $0 |
| Positions before | 4 |
| Positions after | 5 |
| New securities created | 1 |
| Processed events preserved basis | PASS |
| Exceptions flagged | PASS |

The key conclusion:

> The engine processed valid events, created the correct cash movement, added the GEV spin-off position, and preserved total cost basis.

---

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard:

    app.py

The dashboard is designed as a professional operations control room.

It includes five pages:

1. **Executive Control Room**  
   High-level event flow, STP rate, processing status and reconciliation controls.

2. **Portfolio Impact**  
   Before/after cost basis, share quantity changes and final portfolio book.

3. **Exception Management**  
   Supervisor-ready exception queue, reason codes, severity and required actions.

4. **Audit & Reconciliation**  
   Audit trail, cash ledger and basis-preservation checks.

5. **Data Explorer**  
   Interactive inspection and CSV download of all exported tables.

---

## How to Run the Notebook

Clone the repository:

    git clone https://github.com/ludmila-abd/corporate-actions-simulator.git
    cd corporate-actions-simulator

Install dependencies:

    pip install -r requirements.txt

Open Jupyter:

    jupyter notebook Corporate_Actions_Impact_Simulator.ipynb

Then run:

    Kernel → Restart Kernel and Run All Cells

---

## How to Run the Streamlit App

From the project folder:

    streamlit run app.py

The dashboard will open in your browser.

If it does not open automatically, Streamlit will print a local URL such as:

    http://localhost:8501

Open that URL in your browser.

---

## Excel / Reporting Export

The notebook exports a reporting workbook:

    outputs/corporate_actions_powerbi_export.xlsx

The workbook contains:

| Sheet | Description |
|---|---|
| Executive_Summary | Key KPIs and headline results |
| Starting_Portfolio | Original position book |
| Final_Portfolio | Updated portfolio after processing |
| Event_Queue | Full corporate actions feed and processing status |
| Audit_Log | Successfully processed events |
| Exception_Queue | Invalid events routed to review |
| Supervisor_Exceptions | Enriched exception queue with reason codes and SLA status |
| Cash_Ledger | Dividend cash movements |
| Reconciliation | Accounting control checks |
| Position_Comparison | Before/after position comparison |
| KPI_Summary | Processing KPIs |
| Chart_Inventory | List of generated chart files |

---

## Visual Outputs

The notebook also exports chart files:

    outputs/corp_actions_cost_basis_before_after.png
    outputs/corp_actions_shares_before_after.png
    outputs/corp_actions_processing_status.png
    outputs/corp_actions_kpi_dashboard.png
    outputs/corp_actions_exception_reason_codes.png

These visuals support the notebook and dashboard.

---

## Key Takeaways

### 1. Valid events can be automated

The AAPL split, KO dividend and GE spin-off were processed automatically after passing validation.

### 2. Bad data must be stopped early

The MSFT and TSLA events were rejected before they could affect the portfolio.

This is the core operational control.

### 3. Cost basis is the main accounting check

The total cost basis remained unchanged at $286,000 before and after processing.

This confirms that the valid corporate actions changed the structure of the portfolio without creating or destroying accounting value.

### 4. Auditability matters

Every processed event is recorded in an audit log.

This allows a reviewer to trace:

- what changed
- when it changed
- which event caused the change
- whether basis was preserved

### 5. Exception management is part of the product

The project does not only show successful processing.

It also shows what happens when incoming data is wrong.

That makes it closer to a real Asset Services workflow.

---

## Skills Demonstrated

- Python data analysis
- pandas workflow design
- portfolio accounting logic
- corporate actions processing
- cost-basis validation
- exception handling
- audit log design
- reconciliation controls
- KPI reporting
- Excel export automation
- Streamlit dashboard development
- Plotly visualisation
- operational risk framing
- financial operations storytelling

---

## Possible Extensions

Future versions could include:

- rights issues
- stock dividends
- cash-and-stock mergers
- tender offers
- fractional share handling
- withholding tax on dividends
- multi-account processing
- multi-currency portfolios
- custodian vs internal-book reconciliation
- real corporate actions data
- pytest unit tests
- SLA breach simulation
- database storage
- user-uploaded corporate action files

---

## Tech Stack

- Python
- pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- OpenPyXL
- Jupyter Notebook

---

## Disclaimer

This project is an educational simulation.

It is designed to demonstrate corporate actions logic, financial operations controls and exception-management workflows.

It is not connected to live market data, client accounts or production custody systems.

---

## Author

**Ludmila Aboud**  
MSc Economics, Banking & Finance  
MSc Applied Mathematics for Finance
