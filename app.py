import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(page_title="CTI iOS-Glass Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --------------------------------------------------
# IOS GLASSMORPHIC CSS STYLING
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif');

    /* Dark sleek background simulating iOS dark mode wallpaper */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #f8fafc;
    }

    /* Standard Glassmorphism Container */
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

    /* Smaller Glass Card for Metrics */
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
        font-size: 13px;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .glass-metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
    }

    /* Hide default Streamlit styling */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATA GENERATION (Simulating Kaggle Dataset)
# --------------------------------------------------
@st.cache_data
def load_kaggle_mock_data():
    np.random.seed(42)
    n_rows = 5000

    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    timestamps = [start_time + timedelta(minutes=np.random.randint(0, 10080)) for _ in range(n_rows)]

    countries = ["China", "Russia", "USA", "Brazil", "Iran", "North Korea", "Germany", "India", "Vietnam", "Romania"]
    asns = ["AS4134 Chinanet", "AS12389 Rostelecom", "AS7018 AT&T", "AS3320 Deutsche Telekom", "AS15169 Google"]
    ports = [80, 443, 22, 3389, 53, 21, 23, 445]
    services = ["HTTP", "HTTPS", "SSH", "RDP", "DNS", "FTP", "Telnet", "SMB"]
    attack_types = ["DDoS", "Malware", "Brute Force", "SQL Injection", "XSS", "Phishing"]
    protocols = ["TCP", "UDP", "ICMP"]
    rules = ["ET PRO EXPLOIT CVE-2023-46805", "GPL SCAN SSH Brute Force", "SURICATA STREAM 3way handshake",
             "ET TROJAN APT33 C2", "ET MALWARE Win32/CoinMiner"]
    mitre = ["T1190 Exploit Public-Facing App", "T1110 Brute Force", "T1498 Network DoS", "T1059 Command & Scripting",
             "T1071 App Layer Protocol"]

    df = pd.DataFrame({
        "Timestamp": sorted(timestamps),
        "Source IP": [
            f"{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}"
            for _ in range(n_rows)],
        "Destination IP": [f"10.0.{np.random.randint(1, 5)}.{np.random.randint(1, 255)}" for _ in range(n_rows)],
        "Source Country": np.random.choice(countries, n_rows,
                                           p=[0.25, 0.20, 0.15, 0.10, 0.10, 0.05, 0.05, 0.05, 0.025, 0.025]),
        "ASN": np.random.choice(asns, n_rows),
        "Destination Port": np.random.choice(ports, n_rows),
        "Service": np.random.choice(services, n_rows),
        "Traffic Type": np.random.choice(["External", "Internal"], n_rows, p=[0.85, 0.15]),
        "Attack Type": np.random.choice(attack_types, n_rows),
        "Protocol": np.random.choice(protocols, n_rows, p=[0.7, 0.2, 0.1]),
        "IDS Signature": np.random.choice(rules, n_rows),
        "MITRE ATT&CK": np.random.choice(mitre, n_rows),
        "Severity Level": np.random.choice(["Low", "Medium", "High", "Critical"], n_rows, p=[0.4, 0.35, 0.2, 0.05]),
        "Threat Score": np.random.normal(60, 15, n_rows).clip(0, 100).astype(int),
        "Alert Triggered": np.random.choice([True, False], n_rows, p=[0.3, 0.7])
    })
    return df


df = load_kaggle_mock_data()

# Plotly global layout settings
layout_update = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f8fafc", family="-apple-system"),
    margin=dict(t=30, b=30, l=30, r=30)
)

st.markdown(
    '<div class="glass-panel" style="text-align:center;"><div class="glass-header" style="font-size:36px;">Cyber Threat Intelligence</div><div style="color:#94a3b8;">System Telemetry & Advanced Threat Analytics</div></div>',
    unsafe_allow_html=True)

# ==============================================================================
# 1. THE VOLUME LAYER
# ==============================================================================
st.markdown('<div class="glass-header">1. System Volume Layer</div>', unsafe_allow_html=True)

total_events = len(df)
eps = round(total_events / (7 * 24 * 60 * 60), 2)
alerts = df["Alert Triggered"].sum()
incidents = int(alerts * 0.12)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(
    f'<div class="glass-card"><div class="glass-metric-title">Events Ingested</div><div class="glass-metric-value">{total_events:,}</div></div>',
    unsafe_allow_html=True)
with c2: st.markdown(
    f'<div class="glass-card"><div class="glass-metric-title">Events / Second</div><div class="glass-metric-value">{eps}</div></div>',
    unsafe_allow_html=True)
with c3: st.markdown(
    f'<div class="glass-card"><div class="glass-metric-title">Alerts Triggered</div><div class="glass-metric-value">{alerts:,}</div></div>',
    unsafe_allow_html=True)
with c4: st.markdown(
    f'<div class="glass-card"><div class="glass-metric-title">Active Incidents</div><div class="glass-metric-value" style="color:#ef4444;">{incidents:,}</div></div>',
    unsafe_allow_html=True)

# CORRECTED: Changed '4H' to lowercase '4h' for Pandas compatibility
time_df = df.set_index('Timestamp').resample('4h').size().reset_index(name='Events')
fig1 = px.area(time_df, x='Timestamp', y='Events', title="Event Ingestion Trend", color_discrete_sequence=["#3b82f6"])
fig1.update_layout(**layout_update)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 2. SOURCE INTELLIGENCE LAYER
# ==============================================================================
st.markdown('<div class="glass-header">2. Source Intelligence Layer</div>', unsafe_allow_html=True)

unique_ips = df["Source IP"].nunique()
top_ip = df["Source IP"].value_counts().index[0]

# Metrics Row
c1, c2 = st.columns(2)
with c1: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Unique Source IPs</div><div class="glass-metric-value">{unique_ips:,}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Top Attacking IP</div><div class="glass-metric-value" style="color:#f59e0b;">{top_ip}</div></div>', unsafe_allow_html=True)

# Global Threat Map
map_df = df["Source Country"].value_counts().reset_index()
map_df.columns = ["Source Country", "Event Count"]

fig_map = px.choropleth(
    map_df,
    locations="Source Country",
    locationmode="country names",
    color="Event Count",
    color_continuous_scale="magma",
    title="Global Threat Origins (Live Heatmap)"
)

fig_map.update_layout(
    **layout_update,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255, 255, 255, 0.2)",
        projection_type="equirectangular",
        bgcolor='rgba(0,0,0,0)',
        lakecolor='rgba(0,0,0,0)',
        showland=True,
        landcolor='rgba(255, 255, 255, 0.05)'
    )
)
st.plotly_chart(fig_map, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    country_df = df["Source Country"].value_counts().reset_index()
    fig2 = px.bar(country_df, x='Source Country', y='count', title="Top Attacking Countries", color='count', color_continuous_scale="magma")
    fig2.update_layout(**layout_update)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("<div style='font-weight:600; margin-bottom:15px; color:#f8fafc;'>Autonomous System Number (ASN) Distribution</div>", unsafe_allow_html=True)
    asn_df = df["ASN"].value_counts().reset_index().rename(columns={"count": "Event Count"})
    st.dataframe(asn_df, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 3. TARGET LAYER
# ==============================================================================
st.markdown('<div class="glass-header">3. Target Layer</div>', unsafe_allow_html=True)

top_dest_ip = df["Destination IP"].value_counts().index[0]
ext_traffic = df[df["Traffic Type"] == "External"].shape[0]
int_traffic = df[df["Traffic Type"] == "Internal"].shape[0]
ratio = round(ext_traffic / max(int_traffic, 1), 2)
top_service = df["Service"].value_counts().index[0]

# Metrics Row
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Top Targeted IP</div><div class="glass-metric-value">{top_dest_ip}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Ext vs Int Ratio</div><div class="glass-metric-value">{ratio} : 1</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Most Targeted Service</div><div class="glass-metric-value">{top_service}</div></div>', unsafe_allow_html=True)

# Destination Country Logic
if "Destination Country" not in df.columns:
    np.random.seed(101)
    dest_countries = ["USA", "India", "Germany", "Japan", "UK", "Australia", "Canada", "Singapore"]
    df["Destination Country"] = np.random.choice(dest_countries, len(df), p=[0.40, 0.15, 0.10, 0.10, 0.05, 0.05, 0.10, 0.05])

target_map_df = df["Destination Country"].value_counts().reset_index()
target_map_df.columns = ["Destination Country", "Event Count"]

fig_target_map = px.choropleth(
    target_map_df,
    locations="Destination Country",
    locationmode="country names",
    color="Event Count",
    color_continuous_scale="Teal",
    title="Global Attack Destinations"
)

fig_target_map.update_layout(
    **layout_update,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255, 255, 255, 0.2)",
        projection_type="equirectangular",
        bgcolor='rgba(0,0,0,0)',
        lakecolor='rgba(0,0,0,0)',
        showland=True,
        landcolor='rgba(255, 255, 255, 0.05)'
    )
)
st.plotly_chart(fig_target_map, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    port_df = df["Destination Port"].astype(str).value_counts().reset_index()
    fig3 = px.pie(port_df, names='Destination Port', values='count', hole=0.6, title="Target Port Distribution", color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig3.update_layout(**layout_update)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    service_df = df["Service"].value_counts().reset_index()
    fig4 = px.bar(service_df, y='Service', x='count', orientation='h', title="Services Under Pressure", color='count', color_continuous_scale="Blues")
    fig4.update_layout(**layout_update, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)