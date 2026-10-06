# ==============================================================================
# 4. ATTACK BEHAVIOR LAYER
# ==============================================================================
st.markdown('<div class="glass-header">4. Attack Behavior Layer</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    atk_df = df["Attack Type"].value_counts().reset_index()
    fig5 = px.bar(atk_df, x='Attack Type', y='count', title="Attack Type Distribution", color='Attack Type',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig5.update_layout(**layout_update, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    proto_df = df["Protocol"].value_counts().reset_index()
    fig6 = px.pie(proto_df, names='Protocol', values='count', hole=0.4, title="Protocol Distribution")
    fig6.update_layout(**layout_update)
    st.plotly_chart(fig6, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    ids_df = df["IDS Signature"].value_counts().reset_index().head(5)
    fig7 = px.bar(ids_df, y='IDS Signature', x='count', orientation='h', title="Top Triggered IDS Rules",
                  color_discrete_sequence=["#fb7185"])
    fig7.update_layout(**layout_update, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig7, use_container_width=True)

with col4:
    mitre_df = df["MITRE ATT&CK"].value_counts().reset_index()
    fig8 = px.treemap(mitre_df, path=['MITRE ATT&CK'], values='count', title="MITRE ATT&CK Tactic Mapping",
                      color='count', color_continuous_scale="Purples")
    fig8.update_layout(**layout_update)
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 5. RISK AND SEVERITY LAYER
# ==============================================================================
st.markdown('<div class="glass-header">5. Risk & Severity Layer</div>', unsafe_allow_html=True)

# FIX: dynamically calculate end time from the dataset instead of global scope
data_end_time = df["Timestamp"].max()

avg_score = round(df["Threat Score"].mean(), 1)
crit_last_hour = len(df[(df["Severity Level"] == "Critical") & (df["Timestamp"] >= (data_end_time - timedelta(hours=1)))])
max_score = df["Threat Score"].max()

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Avg Threat Score</div><div class="glass-metric-value">{avg_score}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Critical (Last Hour)</div><div class="glass-metric-value" style="color:#ef4444;">{crit_last_hour}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="glass-card"><div class="glass-metric-title">Peak Risk Score</div><div class="glass-metric-value" style="color:#f43f5e;">{max_score}</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    sev_df = df["Severity Level"].value_counts().reset_index()
    fig9 = px.pie(sev_df, names='Severity Level', values='count', title="Event Severity Distribution", color='Severity Level',
                  color_discrete_map={"Critical": "#ef4444", "High": "#f97316", "Medium": "#eab308", "Low": "#22c55e"})
    fig9.update_layout(**layout_update)
    st.plotly_chart(fig9, use_container_width=True)

with col2:
    fig10 = px.histogram(df, x="Threat Score", nbins=50, title="Threat Confidence Score Distribution", color_discrete_sequence=["#8b5cf6"])
    fig10.update_layout(**layout_update)
    st.plotly_chart(fig10, use_container_width=True)

st.markdown("<div class='glass-panel'><div class='glass-header' style='font-size:18px;'>Recent Critical Incident Logs</div>", unsafe_allow_html=True)
crit_table = df[df["Severity Level"] == "Critical"].sort_values(by="Timestamp", ascending=False).head(10)
cols_to_show = ["Timestamp", "Source IP", "Destination IP", "Attack Type", "Threat Score", "IDS Signature"]
st.dataframe(crit_table[cols_to_show], use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#94a3b8; font-size:14px; margin-top:20px;">End of Telemetry Report</div>', unsafe_allow_html=True)