import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Corporate Actions Control Room",
    page_icon="🏦",
    layout="wide",
)

# ============================================================
# THEME CONSTANTS
# ============================================================

INK = "#18181B"
MUTED = "#6B7280"
CREAM = "#F7F3EA"
CARD = "#FFFFFF"
BORDER = "#E7E0D4"
BRONZE = "#8B5E34"
GOLD = "#D6A85F"
TEAL = "#0F766E"
BURGUNDY = "#991B1B"
SLATE = "#334155"
LIGHT_TEAL = "#CCFBF1"
LIGHT_RED = "#FEE2E2"
LIGHT_GOLD = "#FEF3C7"

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at top left, #fffaf0 0%, {CREAM} 34%, #f3eee6 100%);
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2.2rem;
    }}

    section[data-testid="stSidebar"] {{
        background: #1f2933;
        border-right: 1px solid rgba(255,255,255,0.08);
    }}

    section[data-testid="stSidebar"] * {{
        color: #f8fafc;
    }}

    .sidebar-brand {{
        padding: 18px 4px 8px 4px;
        margin-bottom: 10px;
    }}

    .sidebar-brand-title {{
        font-size: 24px;
        font-weight: 850;
        letter-spacing: -0.03em;
        color: white;
    }}

    .sidebar-brand-sub {{
        margin-top: 6px;
        font-size: 13px;
        color: #d1d5db;
        line-height: 1.45;
    }}

    .hero {{
        background:
            linear-gradient(135deg, rgba(24,24,27,0.96), rgba(51,65,85,0.92)),
            radial-gradient(circle at top right, rgba(214,168,95,0.55), rgba(214,168,95,0));
        border: 1px solid rgba(214,168,95,0.35);
        border-radius: 28px;
        padding: 34px 38px;
        margin-bottom: 22px;
        box-shadow: 0 24px 60px rgba(24,24,27,0.18);
        color: white;
    }}

    .eyebrow {{
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(214,168,95,0.45);
        background: rgba(214,168,95,0.14);
        color: #fef3c7;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
        margin-bottom: 14px;
    }}

    .hero h1 {{
        font-size: 44px;
        line-height: 1.02;
        letter-spacing: -0.055em;
        font-weight: 900;
        margin: 0 0 10px 0;
        color: white;
    }}

    .hero p {{
        font-size: 17px;
        line-height: 1.55;
        color: #e5e7eb;
        max-width: 930px;
        margin-bottom: 0;
    }}

    .metric-card {{
        background: rgba(255,255,255,0.92);
        border: 1px solid {BORDER};
        border-radius: 22px;
        padding: 20px 18px;
        min-height: 128px;
        box-shadow: 0 14px 36px rgba(24,24,27,0.07);
        position: relative;
        overflow: hidden;
    }}

    .metric-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, {BRONZE}, {GOLD});
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 850;
        margin-bottom: 12px;
    }}

    .metric-value {{
        color: {INK};
        font-size: 33px;
        font-weight: 900;
        letter-spacing: -0.045em;
    }}

    .metric-note {{
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 8px;
    }}

    .page-title {{
        margin-top: 10px;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: -0.045em;
        color: {INK};
    }}

    .page-subtitle {{
        color: {MUTED};
        font-size: 15px;
        margin-top: 2px;
        margin-bottom: 20px;
    }}

    .panel {{
        background: rgba(255,255,255,0.94);
        border: 1px solid {BORDER};
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 14px 36px rgba(24,24,27,0.06);
        margin-bottom: 20px;
    }}

    .insight {{
        background: #fffaf0;
        border: 1px solid #f3d7a4;
        border-left: 6px solid {BRONZE};
        border-radius: 18px;
        padding: 18px 20px;
        color: {INK};
        box-shadow: 0 10px 28px rgba(139,94,52,0.08);
        margin: 18px 0;
    }}

    .success {{
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-left: 6px solid {TEAL};
        border-radius: 18px;
        padding: 18px 20px;
        color: {INK};
        margin: 18px 0;
    }}

    .risk {{
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 6px solid {BURGUNDY};
        border-radius: 18px;
        padding: 18px 20px;
        color: {INK};
        margin: 18px 0;
    }}

    .badge-pass {{
        display: inline-block;
        padding: 7px 11px;
        border-radius: 999px;
        background: {LIGHT_TEAL};
        color: {TEAL};
        font-size: 12px;
        font-weight: 900;
        margin-right: 7px;
        letter-spacing: 0.04em;
    }}

    .badge-risk {{
        display: inline-block;
        padding: 7px 11px;
        border-radius: 999px;
        background: {LIGHT_RED};
        color: {BURGUNDY};
        font-size: 12px;
        font-weight: 900;
        margin-right: 7px;
        letter-spacing: 0.04em;
    }}

    .badge-neutral {{
        display: inline-block;
        padding: 7px 11px;
        border-radius: 999px;
        background: {LIGHT_GOLD};
        color: {BRONZE};
        font-size: 12px;
        font-weight: 900;
        margin-right: 7px;
        letter-spacing: 0.04em;
    }}

    .flow-card {{
        background: white;
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 10px 30px rgba(24,24,27,0.06);
        text-align: center;
    }}

    .flow-step {{
        color: {MUTED};
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 900;
    }}

    .flow-value {{
        color: {INK};
        font-size: 22px;
        font-weight: 900;
        margin-top: 6px;
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid {BORDER};
    }}

    h1, h2, h3 {{
        color: {INK};
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

DEFAULT_FILE = Path("outputs") / "corporate_actions_powerbi_export.xlsx"

@st.cache_data
def load_workbook(path_or_buffer):
    return pd.read_excel(path_or_buffer, sheet_name=None)

def get_metric(summary_df, metric_name, default=0):
    row = summary_df.loc[summary_df["metric"] == metric_name, "value"]
    if len(row) == 0:
        return default
    return row.iloc[0]

def as_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default

def fmt_num(value):
    return f"{as_float(value):,.0f}"

def fmt_money(value):
    return f"${as_float(value):,.2f}"

def fmt_pct(value):
    return f"{as_float(value):.1%}"

def page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def flow_card(step, value):
    st.markdown(
        f"""
        <div class="flow-card">
            <div class="flow-step">{step}</div>
            <div class="flow-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def style_fig(fig, height=420):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=24, r=24, t=68, b=34),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Arial, sans-serif", size=13, color=INK),
        title=dict(font=dict(size=19, color=INK, family="Inter, Arial, sans-serif")),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5E7EB")
    fig.update_yaxes(gridcolor="#EEE7DA", zerolinecolor="#EEE7DA")
    return fig

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">CA Control Room</div>
        <div class="sidebar-brand-sub">
            Corporate actions processing, exception control and reconciliation dashboard.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.sidebar.file_uploader("Upload Excel export", type=["xlsx"])

if uploaded_file is not None:
    data_source = uploaded_file
    st.sidebar.success("Workbook uploaded")
elif DEFAULT_FILE.exists():
    data_source = DEFAULT_FILE
    st.sidebar.success("Using local export")
else:
    st.sidebar.error("Excel export not found. Run the notebook export cell first.")
    st.stop()

sheets = load_workbook(data_source)

required = [
    "Executive_Summary",
    "Final_Portfolio",
    "Event_Queue",
    "Audit_Log",
    "Supervisor_Exceptions",
    "Cash_Ledger",
    "Reconciliation",
    "Position_Comparison",
    "KPI_Summary",
]

missing = [s for s in required if s not in sheets]
if missing:
    st.error(f"Missing required sheet(s): {missing}")
    st.stop()

executive = sheets["Executive_Summary"]
final_portfolio = sheets["Final_Portfolio"]
event_queue = sheets["Event_Queue"]
audit_log = sheets["Audit_Log"]
supervisor_exceptions = sheets["Supervisor_Exceptions"]
cash_ledger = sheets["Cash_Ledger"]
reconciliation = sheets["Reconciliation"]
position_comparison = sheets["Position_Comparison"]
kpi_summary = sheets["KPI_Summary"]

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Control Room",
        "Portfolio Impact",
        "Exception Management",
        "Audit & Reconciliation",
        "Data Explorer",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Built with Python, pandas, Plotly and Streamlit.")

# ============================================================
# METRICS
# ============================================================

events_received = get_metric(executive, "Events Received")
events_processed = get_metric(executive, "Events Processed")
events_flagged = get_metric(executive, "Events Flagged")
stp_rate = get_metric(executive, "Straight-Through Processing Rate")
exception_rate = get_metric(executive, "Exception Rate")
cash_generated = get_metric(executive, "Cash Generated")
cost_basis_diff = get_metric(executive, "Cost Basis Difference")
positions_after = get_metric(executive, "Positions After")
new_sec = get_metric(executive, "New Securities Created")

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Asset Services Simulation</div>
        <h1>Corporate Actions Control Room</h1>
        <p>
            A professional operations dashboard for processing stock splits, dividends and spin-offs,
            with validation controls, exception management, cash ledger updates, audit trail and
            reconciliation reporting.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# KPI STRIP

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)

with m1:
    metric_card("Received", fmt_num(events_received), "feed events")
with m2:
    metric_card("Processed", fmt_num(events_processed), "auto-applied")
with m3:
    metric_card("Flagged", fmt_num(events_flagged), "manual review")
with m4:
    metric_card("STP Rate", fmt_pct(stp_rate), "automation")
with m5:
    metric_card("Exception Rate", fmt_pct(exception_rate), "control breaks")
with m6:
    metric_card("Cash", fmt_money(cash_generated), "dividend ledger")
with m7:
    metric_card("Basis Break", fmt_money(cost_basis_diff), "reconciled")

st.write("")

# ============================================================
# PAGE 1 — EXECUTIVE CONTROL ROOM
# ============================================================

if page == "Executive Control Room":
    page_header(
        "Executive Control Room",
        "A one-page operating view of event flow, straight-through processing and reconciliation status."
    )

    st.markdown(
        """
        <span class="badge-pass">COST BASIS RECONCILED</span>
        <span class="badge-neutral">GEV POSITION CREATED</span>
        <span class="badge-risk">2 ITEMS FOR REVIEW</span>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    f1, f2, f3, f4, f5 = st.columns(5)
    with f1:
        flow_card("01 Incoming Feed", "5 events")
    with f2:
        flow_card("02 Validation", "3 pass / 2 fail")
    with f3:
        flow_card("03 Processing", "3 applied")
    with f4:
        flow_card("04 Controls", "$0 basis break")
    with f5:
        flow_card("05 Review Queue", "2 exceptions")

    st.write("")

    c1, c2 = st.columns([1.1, 0.9])

    with c1:
        status_counts = event_queue["processing_status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]

        fig_status = px.bar(
            status_counts,
            x="status",
            y="count",
            text="count",
            color="status",
            color_discrete_map={
                "PROCESSED": TEAL,
                "FLAGGED": BURGUNDY,
            },
            title="Processed vs Flagged Events",
        )
        fig_status.update_traces(textposition="outside", marker_line_width=0)
        fig_status.update_layout(showlegend=False)
        fig_status = style_fig(fig_status, 430)
        st.plotly_chart(fig_status, use_container_width=True)

    with c2:
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=as_float(stp_rate) * 100,
                number={
                    "suffix": "%",
                    "font": {"size": 44, "color": INK},
                },
                title={"text": "Straight-Through Processing Rate"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": BRONZE},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 50], "color": "#FEE2E2"},
                        {"range": [50, 80], "color": "#FEF3C7"},
                        {"range": [80, 100], "color": "#CCFBF1"},
                    ],
                },
            )
        )
        fig_gauge = style_fig(fig_gauge, 430)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown(
        """
        <div class="insight">
            <b>Executive takeaway:</b> the processing cycle completed successfully.
            Valid events were processed, invalid events were isolated, dividend cash was generated,
            and total cost basis reconciled back to the starting portfolio.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Reconciliation Controls")
    st.dataframe(reconciliation, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 2 — PORTFOLIO IMPACT
# ============================================================

elif page == "Portfolio Impact":
    page_header(
        "Portfolio Impact",
        "Before/after view of how corporate actions changed the position book."
    )

    c1, c2 = st.columns(2)

    with c1:
        fig_basis = px.bar(
            position_comparison,
            x="ticker",
            y=["cost_basis_before", "cost_basis_after"],
            barmode="group",
            title="Cost Basis Before vs After",
            labels={"value": "Cost Basis ($)", "ticker": "Ticker", "variable": ""},
            color_discrete_sequence=["#C7B8A1", BRONZE],
        )
        fig_basis = style_fig(fig_basis, 440)
        st.plotly_chart(fig_basis, use_container_width=True)

    with c2:
        fig_shares = px.bar(
            position_comparison,
            x="ticker",
            y=["shares_before", "shares_after"],
            barmode="group",
            title="Share Quantity Before vs After",
            labels={"value": "Shares", "ticker": "Ticker", "variable": ""},
            color_discrete_sequence=["#CBD5E1", SLATE],
        )
        fig_shares = style_fig(fig_shares, 440)
        st.plotly_chart(fig_shares, use_container_width=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        metric_card("Final Positions", fmt_num(positions_after), "portfolio book")
    with s2:
        metric_card("New Security", fmt_num(new_sec), "GEV spin-off")
    with s3:
        metric_card("Cost Basis Break", fmt_money(cost_basis_diff), "control result")

    st.markdown("### Final Portfolio Book")

    cols = [
        col for col in [
            "ticker", "company_name", "shares", "avg_cost",
            "cost_basis_total", "market_value", "portfolio_weight"
        ]
        if col in final_portfolio.columns
    ]

    st.dataframe(final_portfolio[cols], use_container_width=True, hide_index=True)

    st.markdown(
        """
        <div class="success">
            <b>Portfolio takeaway:</b> AAPL changed structure through the split, GE created a new GEV position,
            KO generated cash, and MSFT stayed unchanged because the invalid split was blocked.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PAGE 3 — EXCEPTION MANAGEMENT
# ============================================================

elif page == "Exception Management":
    page_header(
        "Exception Management",
        "Supervisor-ready control view of flagged events, reason codes, severity and next actions."
    )

    if supervisor_exceptions.empty:
        st.success("No exceptions requiring supervisor review.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            reason_counts = supervisor_exceptions["reason_code"].value_counts().reset_index()
            reason_counts.columns = ["reason_code", "count"]

            fig_reason = px.bar(
                reason_counts,
                y="reason_code",
                x="count",
                orientation="h",
                text="count",
                color="reason_code",
                title="Exceptions by Reason Code",
                color_discrete_sequence=[BURGUNDY, BRONZE, GOLD],
            )
            fig_reason.update_traces(textposition="outside", marker_line_width=0)
            fig_reason.update_layout(showlegend=False)
            fig_reason = style_fig(fig_reason, 430)
            st.plotly_chart(fig_reason, use_container_width=True)

        with c2:
            severity_counts = supervisor_exceptions["severity"].value_counts().reset_index()
            severity_counts.columns = ["severity", "count"]

            fig_sev = px.pie(
                severity_counts,
                names="severity",
                values="count",
                hole=0.58,
                title="Exception Severity Mix",
                color="severity",
                color_discrete_map={
                    "LOW": TEAL,
                    "MEDIUM": GOLD,
                    "HIGH": BURGUNDY,
                    "CRITICAL": "#450A0A",
                },
            )
            fig_sev = style_fig(fig_sev, 430)
            st.plotly_chart(fig_sev, use_container_width=True)

        st.markdown(
            """
            <div class="risk">
                <b>Control takeaway:</b> flagged records failed for different reasons.
                MSFT has invalid event terms, while TSLA is an eligibility break.
                Both are stopped before they affect client positions or cash.
            </div>
            """,
            unsafe_allow_html=True,
        )

        f1, f2, f3 = st.columns(3)

        with f1:
            reason = st.multiselect(
                "Reason code",
                sorted(supervisor_exceptions["reason_code"].dropna().unique()),
                default=sorted(supervisor_exceptions["reason_code"].dropna().unique()),
            )

        with f2:
            severity = st.multiselect(
                "Severity",
                sorted(supervisor_exceptions["severity"].dropna().unique()),
                default=sorted(supervisor_exceptions["severity"].dropna().unique()),
            )

        with f3:
            sla = st.multiselect(
                "SLA status",
                sorted(supervisor_exceptions["sla_status"].dropna().unique()),
                default=sorted(supervisor_exceptions["sla_status"].dropna().unique()),
            )

        filtered = supervisor_exceptions[
            supervisor_exceptions["reason_code"].isin(reason)
            & supervisor_exceptions["severity"].isin(severity)
            & supervisor_exceptions["sla_status"].isin(sla)
        ]

        display_cols = [
            col for col in [
                "event_id", "ticker", "action_type", "issue",
                "reason_code", "severity", "sla_status",
                "review_owner", "required_action"
            ]
            if col in filtered.columns
        ]

        st.markdown("### Supervisor Exception Queue")
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

# ============================================================
# PAGE 4 — AUDIT & RECONCILIATION
# ============================================================

elif page == "Audit & Reconciliation":
    page_header(
        "Audit & Reconciliation",
        "Traceable record of processed events, cash movements and accounting controls."
    )

    st.markdown("### Audit Trail")

    audit_cols = [
        col for col in [
            "event_id", "ticker", "action_type", "status",
            "shares_before", "shares_after",
            "avg_cost_before", "avg_cost_after",
            "cost_basis_before", "cost_basis_after",
            "cash_generated", "new_ticker", "basis_preserved"
        ]
        if col in audit_log.columns
    ]

    st.dataframe(audit_log[audit_cols], use_container_width=True, hide_index=True)

    c1, c2 = st.columns([1.05, 0.95])

    with c1:
        st.markdown("### Cash Ledger")
        if cash_ledger.empty:
            st.info("No cash movements generated.")
        else:
            cash_cols = [
                col for col in [
                    "event_id", "ticker", "action_type",
                    "cash_amount_per_share", "shares_eligible",
                    "cash_generated", "currency"
                ]
                if col in cash_ledger.columns
            ]
            st.dataframe(cash_ledger[cash_cols], use_container_width=True, hide_index=True)

    with c2:
        basis_counts = audit_log["basis_preserved"].value_counts().reset_index()
        basis_counts.columns = ["basis_preserved", "count"]
        basis_counts["basis_preserved"] = basis_counts["basis_preserved"].astype(str)

        fig = px.pie(
            basis_counts,
            names="basis_preserved",
            values="count",
            hole=0.62,
            title="Basis Preservation Check",
            color="basis_preserved",
            color_discrete_map={"True": TEAL, "False": BURGUNDY},
        )
        fig = style_fig(fig, 360)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="insight">
            <b>Audit takeaway:</b> the system keeps a full record of every processed event,
            separates position changes from cash movements, and confirms basis preservation.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PAGE 5 — DATA EXPLORER
# ============================================================

elif page == "Data Explorer":
    page_header(
        "Data Explorer",
        "Inspect and export any table created by the processing engine."
    )

    table = st.selectbox("Select table", sorted(sheets.keys()))
    st.dataframe(sheets[table], use_container_width=True, hide_index=True)

    st.download_button(
        "Download selected table as CSV",
        data=sheets[table].to_csv(index=False).encode("utf-8"),
        file_name=f"{table}.csv",
        mime="text/csv",
    )
