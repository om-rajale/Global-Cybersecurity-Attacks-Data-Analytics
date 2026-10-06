import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Cyber Attack Analytics Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #f8fafc;
}
.glass-panel {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
}
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
    text-align: center;
}
.glass-header {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 16px;
    background: -webkit-linear-gradient(45deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.glass-metric-title {
    font-size: 13px; font-weight: 500; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
}
.glass-metric-value { font-size: 32px; font-weight: 700; color: #ffffff; }
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATA LOADING (real CSV, no random data)
# --------------------------------------------------
CSV_PATH = "cybersecurity_attacks.csv"

# Left side = column name in YOUR csv, right side = name used by this dashboard.
# Run  print(pd.read_csv(CSV_PATH).columns.tolist())  and edit the LEFT side if yours differ.
COLUMN_MAP = {
    "Timestamp": "Timestamp",
    "Source IP Address": "Source IP",
    "Destination IP Address": "Destination IP",
    "Destination Port": "Destination Port",
    "Protocol": "Protocol",
    "Traffic Type": "Traffic Type",
    "Attack Type": "Attack Type",
    "Severity Level": "Severity Level",
    "Alerts/Warnings": "Alerts",
    "Geo-location Data": "Location",
}


@st.cache_data
def load_data():
    raw = pd.read_csv(CSV_PATH)
    missing = [c for c in COLUMN_MAP if c not in raw.columns]
    if missing:
        st.error(f"These columns were not found in the CSV: {missing}")
        st.write("Columns in your CSV:", raw.columns.tolist())
        st.stop()

    df = raw[list(COLUMN_MAP)].rename(columns=COLUMN_MAP)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp")
    df["Destination Port"] = pd.to_numeric(df["Destination Port"], errors="coerce")
    # In this dataset a blank Alerts/Warnings cell means no alert was raised
    df["Alert Triggered"] = df["Alerts"].astype(str).str.contains("alert", case=False, na=False)
    return df.reset_index(drop=True)


df = load_data()
layout_update = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f8fafc"), margin=dict(t=40, b=30, l=30, r=30),
)


def metric(col, title, value, color="#ffffff"):
    col.markdown(
        f'<div class="glass-card"><div class="glass-metric-title">{title}</div>'
        f'<div class="glass-metric-value" style="color:{color};">{value}</div></div>',
        unsafe_allow_html=True)


st.markdown(
    '<div class="glass-panel" style="text-align:center;"><div class="glass-header" style="font-size:36px;">'
    'Cyber Attack Analytics</div><div style="color:#94a3b8;">Network telemetry from cybersecurity_attacks.csv'
    '</div></div>', unsafe_allow_html=True)

# ---------------- 1. VOLUME ----------------
st.markdown('<div class="glass-header">1. Volume Layer</div>', unsafe_allow_html=True)
span_days = max((df["Timestamp"].max() - df["Timestamp"].min()).days, 1)
high_sev = int(df["Severity Level"].isin(["High", "Critical"]).sum())

c1, c2, c3, c4 = st.columns(4)
metric(c1, "Events Ingested", f"{len(df):,}")
metric(c2, "Avg Events / Day", f"{len(df) / span_days:,.1f}")
metric(c3, "Alerts Triggered", f"{int(df['Alert Triggered'].sum()):,}")
metric(c4, "High-Severity Events", f"{high_sev:,}", "#ef4444")

time_df = df.set_index("Timestamp").resample("W").size().reset_index(name="Events")
fig1 = px.area(time_df, x="Timestamp", y="Events", title="Weekly Event Trend", color_discrete_sequence=["#3b82f6"])
fig1.update_layout(**layout_update)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- 2. SOURCE ----------------
st.markdown('<div class="glass-header">2. Source Intelligence Layer</div>', unsafe_allow_html=True)
top_ips = df["Source IP"].value_counts().head(10).reset_index()
top_ips.columns = ["Source IP", "Events"]

c1, c2 = st.columns(2)
metric(c1, "Unique Source IPs", f"{df['Source IP'].nunique():,}")
metric(c2, "Top Attacking IP", top_ips.iloc[0, 0], "#f59e0b")

col1, col2 = st.columns(2)
with col1:
    loc_df = df["Location"].value_counts().head(10).reset_index()
    loc_df.columns = ["Location", "Events"]
    fig2 = px.bar(loc_df, x="Location", y="Events", title="Top 10 Source Locations",
                  color="Events", color_continuous_scale="magma")
    fig2.update_layout(**layout_update)
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.markdown("<div style='font-weight:600; margin-bottom:15px;'>Top 10 Attacking IPs</div>", unsafe_allow_html=True)
    st.dataframe(top_ips, use_container_width=True, hide_index=True)

# ---------------- 3. TARGET ----------------
st.markdown('<div class="glass-header">3. Target Layer</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
metric(c1, "Top Targeted IP", df["Destination IP"].value_counts().index[0])
metric(c2, "Most Common Attack", df["Attack Type"].value_counts().index[0])
metric(c3, "Most Targeted Service", df["Traffic Type"].value_counts().index[0])

col1, col2 = st.columns(2)
with col1:
    atk = df["Attack Type"].value_counts().reset_index()
    atk.columns = ["Attack Type", "Events"]
    fig3 = px.pie(atk, names="Attack Type", values="Events", hole=0.6, title="Attack Type Distribution",
                  color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig3.update_layout(**layout_update)
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    svc = df["Traffic Type"].value_counts().reset_index()
    svc.columns = ["Service", "Events"]
    fig4 = px.bar(svc, y="Service", x="Events", orientation="h", title="Services Under Pressure",
                  color="Events", color_continuous_scale="Blues")
    fig4.update_layout(**layout_update, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig4, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    sev = df["Severity Level"].value_counts().reset_index()
    sev.columns = ["Severity", "Events"]
    fig5 = px.bar(sev, x="Severity", y="Events", title="Events by Severity",
                  color="Severity", color_discrete_sequence=px.colors.qualitative.Set2)
    fig5.update_layout(**layout_update)
    st.plotly_chart(fig5, use_container_width=True)
with col2:
    port = df["Destination Port"].dropna().astype(int).astype(str).value_counts().head(10).reset_index()
    port.columns = ["Port", "Events"]
    fig6 = px.bar(port, x="Port", y="Events", title="Top 10 Destination Ports",
                  color="Events", color_continuous_scale="Teal")
    fig6.update_layout(**layout_update)
    st.plotly_chart(fig6, use_container_width=True)
