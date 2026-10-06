import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64
import json
from datetime import datetime

# Set up page config
st.set_page_config(
    page_title="RHBSciAdvisory | Quantum Cryptographic Exposure Analyzer",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Theme and Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stAppHeader {
        background-color: #0b1a30;
    }
    h1, h2, h3 {
        color: #0b1a30;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        text-align: center;
    }
    .report-card {
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 6px solid;
    }
    .critical {
        background-color: #ffeef0;
        border-left-color: #d9534f;
        color: #721c24;
    }
    .high {
        background-color: #fff4e5;
        border-left-color: #fd7e14;
        color: #856404;
    }
    .thin {
        background-color: #fff9db;
        border-left-color: #f0ad4e;
        color: #856404;
    }
    .secure {
        background-color: #ebfbee;
        border-left-color: #5cb85c;
        color: #155724;
    }
    .disclaimer-box {
        background-color: #e9ecef;
        padding: 12px 16px;
        border-radius: 6px;
        border-left: 4px solid #6c757d;
        font-size: 0.9em;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("🔒 Quantum Cryptographic Exposure Analyzer")
st.caption("Audited Mosca's Inequality Risk Modeler ($x + y > z$) | RHBSciAdvisory GmbH Enterprise Advisory Suite")

# Governance Disclaimer
st.markdown("""
<div class='disclaimer-box'>
<b>⚠️ Governance Audit Disclaimer & Methodology Alignment:</b><br>
This diagnostic tool evaluates enterprise exposure to <b>Harvest Now, Decrypt Later (HNDL)</b> threats using 
<b>Mosca's Timing Inequality</b> ($x + y > z$, Mosca 2015). Variable definitions are aligned directly with primary literature: 
<b>x</b> = Confidentiality Span / Security Shelf-Life, <b>y</b> = Migration Timeline, and <b>z</b> = Threat Horizon. 
Signed Slack ($s = z - (x + y)$) determines risk posture. This tool is an enterprise timing predicate for governance, not a hardware forecast or formal compliance certification.
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.image("https://img.icons8.com/color/96/shield-against-piracy.png", width=64)
st.sidebar.title("⚙️ Simulation Controls")

st.sidebar.markdown("### Threat Horizon Scenario (z)")
z_scenario = st.sidebar.selectbox(
    "Select Threat Horizon Scenario:",
    ["Central Consensus (~12 yrs)", "Aggressive CRQC (~8 yrs)", "Conservative (~20 yrs)", "Custom"],
    index=0,
    help="Pre-configured scenarios reflecting expert consensus distributions (e.g., Global Risk Institute) or custom horizon."
)

if z_scenario == "Aggressive CRQC (~8 yrs)":
    default_z = 8
elif z_scenario == "Conservative (~20 yrs)":
    default_z = 20
elif z_scenario == "Central Consensus (~12 yrs)":
    default_z = 12
else:
    default_z = 12

z = st.sidebar.slider(
    "Threat Horizon (z) — Years until CRQC:",
    min_value=1,
    max_value=30,
    value=default_z,
    help="Estimated timeline until a Cryptographically Relevant Quantum Computer (CRQC) capable of breaking RSA-2048/ECC emerges. Default 12 yrs represents expert consensus assumption."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Client Policy Parameters")
custom_name = st.sidebar.text_input("Client Organization / Sector Name:", "Custom Enterprise")

x = st.sidebar.slider(
    "Confidentiality Span (x) — Data Secrecy Lifespan (yrs):",
    min_value=0,
    max_value=100,
    value=15,
    help="Mosca's x: How long encrypted records must remain confidential past creation date due to statutory, IP, or compliance rules (0 allowed for real-time/transient data)."
)

y = st.sidebar.slider(
    "Migration Timeline (y) — Years to deploy PQC (yrs):",
    min_value=0,
    max_value=30,
    value=5,
    help="Mosca's y: Time required to conduct a CBOM audit, refactor systems, and fully deploy Post-Quantum Cryptography (0 allowed for fully agile/migrated systems)."
)

# Standard Industry Presets (Mosca 2015 / Audit Benchmark Data)
default_data = [
    {
        "Client Sector": "Public Research Hospital",
        "Confidentiality Span (x)": 50,
        "Migration Timeline (y)": 6,
        "Description": "Genomic IP & patient records (50-yr statutory protection)"
    },
    {
        "Client Sector": "Tier-1 Retail Bank",
        "Confidentiality Span (x)": 25,
        "Migration Timeline (y)": 8,
        "Description": "SWIFT wire history, core ledger & long-term retention archives"
    },
    {
        "Client Sector": "Municipal Government",
        "Confidentiality Span (x)": 10,
        "Migration Timeline (y)": 5,
        "Description": "Citizen registries & tax infrastructure"
    },
    {
        "Client Sector": "E-Commerce Retailer",
        "Confidentiality Span (x)": 3,
        "Migration Timeline (y)": 2,
        "Description": "Transient session logs & short-lived payment tokens"
    }
]

# Insert Custom Client Profile
all_sectors = default_data.copy()
all_sectors.insert(0, {
    "Client Sector": f"*{custom_name} (Custom)*",
    "Confidentiality Span (x)": x,
    "Migration Timeline (y)": y,
    "Description": "User-defined custom organizational parameters"
})

df = pd.DataFrame(all_sectors)
df["Threat Horizon (z)"] = z
df["Total Target Span (x + y)"] = df["Confidentiality Span (x)"] + df["Migration Timeline (y)"]
df["Signed Slack (s = z - (x+y))"] = df["Threat Horizon (z)"] - df["Total Target Span (x + y)"]
df["Exposure Deficit (d)"] = df["Total Target Span (x + y)"] - df["Threat Horizon (z)"]
df["Inequality Triggered (x+y > z)"] = df["Total Target Span (x + y)"] > df["Threat Horizon (z)"]

# Risk Classification Function using Signed Slack s = z - (x + y)
def classify_risk(row):
    s = row["Signed Slack (s = z - (x+y))"]
    if s < -10:
        return "CRITICAL DEFICIT"
    elif -10 <= s < 0:
        return "HIGH DEFICIT"
    elif 0 <= s <= 5:
        return "THIN MARGIN"
    else:
        return "SECURE MARGIN"

df["Risk Tier"] = df.apply(classify_risk, axis=1)

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Dashboard", 
    "🗺️ Interactive Risk Boundary Map", 
    "📋 Tailored PQC & CBOM Action Plan", 
   
])

# TAB 1: EXECUTIVE DASHBOARD
with tab1:
    st.markdown("### 🔑 Executive Summary KPI Cards")
    
    custom_row = df.iloc[0]
    c_s = custom_row['Signed Slack (s = z - (x+y))']
    c_d = custom_row['Exposure Deficit (d)']
    c_tier = custom_row['Risk Tier']
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.metric(label="Target Span (x + y)", value=f"{custom_row['Total Target Span (x + y)']} yrs")
    with m_col2:
        st.metric(label="Threat Horizon (z)", value=f"{z} yrs")
    with m_col3:
        if c_s < 0:
            st.metric(label="Signed Exposure Deficit (d)", value=f"+{c_d} yrs deficit", delta=f"-{c_d} yrs overhang", delta_color="inverse")
        else:
            st.metric(label="Signed Security Slack (s)", value=f"+{c_s} yrs safe", delta=f"+{c_s} yrs buffer", delta_color="normal")
    with m_col4:
        st.metric(label="Calculated Risk Tier", value=c_tier)

    st.markdown("---")
    st.markdown("### 🏛️ Industry Sector Risk Matrix")
    
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        st.markdown("#### Published Tier Thresholds & Sector Status")
        
        for _, row in df.iterrows():
            s_name = row["Client Sector"]
            s_x = row["Confidentiality Span (x)"]
            s_y = row["Migration Timeline (y)"]
            s_span = row["Total Target Span (x + y)"]
            s_slack = row["Signed Slack (s = z - (x+y))"]
            s_deficit = row["Exposure Deficit (d)"]
            s_tier = row["Risk Tier"]
            
            if s_tier == "CRITICAL DEFICIT":
                c_class = "critical"
                s_msg = f"🚨 <b>CRITICAL EXPOSURE DEFICIT (+{s_deficit} yrs overhang):</b> Mosca's inequality is triggered ($x+y > z$). Encrypted records captured today will be retroactively decrypted **{s_deficit} years** before PQC migration completes!"
            elif s_tier == "HIGH DEFICIT":
                c_class = "high"
                s_msg = f"⚠️ <b>HIGH EXPOSURE DEFICIT (+{s_deficit} yrs overhang):</b> Active HNDL risk! Your total target span exceeds the quantum horizon by **{s_deficit} years**. Accelerated CBOM discovery and hybrid PQC cutover required."
            elif s_tier == "THIN MARGIN":
                c_class = "thin"
                s_msg = f"⚡ <b>THIN SECURITY MARGIN ({s_slack} yrs safe):</b> Security buffer is narrow ($s = {s_slack}$ yrs). Immediate CBOM auditing and PQC migration planning required to prevent deficit."
            else:
                c_class = "secure"
                s_msg = f"✅ <b>SECURE MARGIN ({s_slack} yrs safe):</b> Safe security buffer ($s = {s_slack}$ yrs). Total target span is within the projected quantum threat horizon."
                
            st.markdown(f"""
                <div class='report-card {c_class}'>
                    <h4 style='margin-bottom:4px;'>{s_name}</h4>
                    <p style='margin-bottom:6px;'><b>Confidentiality (x):</b> {s_x} yrs | <b>Migration (y):</b> {s_y} yrs | <b>Target Span (x+y):</b> {s_span} yrs | <b>Horizon (z):</b> {z} yrs</p>
                    <p style='margin-bottom:0px;'>{s_msg}</p>
                </div>
            """, unsafe_with_html=True)
            
    with col_b:
        st.markdown("#### 📥 Audit-Grade Export Data")
        st.dataframe(df[["Client Sector", "Confidentiality Span (x)", "Migration Timeline (y)", "Signed Slack (s = z - (x+y))", "Risk Tier"]], use_container_width=True)
        
        # Enhanced Audit Export
        df_export = df.copy()
        df_export["Audit Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_export["Formula Evaluated"] = "x + y > z"
        df_export["Threat Horizon Provenance"] = f"Scenario: {z_scenario} (z = {z} yrs)"
        
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Full Audit Report (CSV)",
            data=csv,
            file_name="quantum_exposure_audit_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("""
        **Published Tier Definitions:**
        *   **CRITICAL DEFICIT:** $s < -10$ (Deficit $>10$ yrs)
        *   **HIGH DEFICIT:** $-10 \\le s < 0$ (Deficit $1-10$ yrs)
        *   **THIN MARGIN:** $0 \\le s \\le 5$ (Slack $0-5$ yrs)
        *   **SECURE MARGIN:** $s > 5$ (Slack $>5$ yrs)
        """)

# TAB 2: INTERACTIVE RISK MAP
with tab2:
    st.markdown("### 🗺️ Interactive Plotly Mosca Boundary Map")
    st.caption("Geometry: Horizontal Axis = Migration Timeline (y), Vertical Axis = Confidentiality Span (x). Security Boundary Line: x + y = z.")
    
    fig = go.Figure()
    
    # Add Security Boundary Line (x + y = z  =>  x = z - y)
    y_line = np.linspace(0, 20, 100)
    x_line = z - y_line
    
    fig.add_trace(go.Scatter(
        x=y_line, y=x_line,
        mode='lines',
        name=f'Security Boundary (x + y = {z})',
        line=dict(color='#343a40', width=2.5, dash='dash')
    ))
    
    # Add Shaded Regions for Risk Levels
    y_grid = np.linspace(0, 20, 100)
    x_grid = np.linspace(0, 60, 100)
    Y_mesh, X_grid = np.meshgrid(y_grid, x_grid)
    S_mesh = z - (X_grid + Y_mesh)
    
    color_map = {
        "CRITICAL DEFICIT": "#d9534f",
        "HIGH DEFICIT": "#fd7e14",
        "THIN MARGIN": "#f0ad4e",
        "SECURE MARGIN": "#5cb85c"
    }
    
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Migration Timeline (y)"]],
            y=[row["Confidentiality Span (x)"]],
            mode='markers+text',
            name=row["Client Sector"].replace("*", ""),
            text=[row["Client Sector"].replace("*", "")],
            textposition="top right",
            marker=dict(
                size=16,
                color=color_map[row["Risk Tier"]],
                line=dict(width=2, color='DarkSlateGrey')
            ),
            hovertemplate=(
                f"<b>{row['Client Sector']}</b><br>" +
                f"Confidentiality Span (x): {row['Confidentiality Span (x)']} yrs<br>" +
                f"Migration Time (y): {row['Migration Timeline (y)']} yrs<br>" +
                f"Total Target Span (x+y): {row['Total Target Span (x + y)']} yrs<br>" +
                f"Signed Slack (s): <b>{row['Signed Slack (s = z - (x+y))']} yrs</b><br>" +
                f"Risk Tier: <b>{row['Risk Tier']}</b><extra></extra>"
            )
        ))
        
    fig.update_layout(
        title=dict(text=f"Mosca's Inequality Boundary Mapping (Threat Horizon z = {z} Years)", font=dict(size=16)),
        xaxis_title="Migration Timeline in Years (y)",
        yaxis_title="Data Confidentiality Span in Years (x)",
        xaxis=dict(range=[0, 15], gridcolor="#e9ecef"),
        yaxis=dict(range=[0, 60], gridcolor="#e9ecef"),
        template="plotly_white",
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: DYNAMIC ACTION PLAN
with tab3:
    st.markdown("### 🛡️ Gap-Driven PQC & CBOM Remediation Directives")
    
    custom_tier = custom_row['Risk Tier']
    custom_deficit = custom_row['Exposure Deficit (d)']
    custom_slack = custom_row['Signed Slack (s = z - (x+y))']
    
    st.info(f"💡 **Active Client Remediation Context:** Currently analyzing **{custom_name}** ({custom_tier} | Deficit: {custom_deficit} yrs | Signed Slack: {custom_slack} yrs). Action directives dynamically adapt to your exposure status.")
    
    c_p1, c_p2 = st.columns(2)
    
    with c_p1:
        st.markdown("#### 1. Urgent Action Directives for Active Client Status")
        if custom_tier in ["CRITICAL DEFICIT", "HIGH DEFICIT"]:
            st.error(f"""
            **🚨 IMMEDIATE HNDL REMEDIATION MANDATORY (Exposure Deficit: +{custom_deficit} yrs)**
            1. **Launch Automated CBOM Discovery (Wave 0):** Deploy SAST and dependency scanners to catalog asymmetric algorithms (RSA, ECC, ECDH) across internet-facing TLS gateways, database connections, and long-lived backup stores.
            2. **Prioritize Key Encapsulation (ML-KEM):** Immediately deploy **ML-KEM (FIPS 203 / CRYSTALS-Kyber)** in hybrid mode (e.g., X25519 + ML-KEM-768) to protect data-in-transit against active Harvest Now, Decrypt Later interception.
            3. **Executive Governance Escalation:** Present the signed exposure deficit (+{custom_deficit} yrs) to the Board / CISO to secure dedicated PQC migration funding.
            """)
        elif custom_tier == "THIN MARGIN":
            st.warning(f"""
            **⚡ PREEMPTIVE CBOM & HYBRID MIGRATION (Thin Slack: +{custom_slack} yrs)**
            1. **Complete CBOM Asset Inventory:** Audit public-key dependencies across software composition analysis (SCA) and Hardware Security Modules (HSMs).
            2. **Draft Hybrid Cutover Plan:** Prepare hybrid PQC wrappers for key exchange (ML-KEM) and digital signatures (ML-DSA) before the margin turns negative.
            3. **Vendor Questionnaire Dispatch:** Issue PQC readiness questionnaires to third-party SaaS/PaaS suppliers.
            """)
        else:
            st.success(f"""
            **✅ ROUTINE CRYPTO-AGILITY & MAINTENANCE (Secure Slack: +{custom_slack} yrs)**
            1. **Maintain Cryptographic Bill of Materials (CBOM):** Embed automated scanning into CI/CD build pipelines to prevent legacy RSA/ECC algorithms from re-entering production.
            2. **Refactor for Crypto-Agility:** Abstract security interfaces so algorithm parameter sets can be swapped without application refactoring.
            3. **Track Regulatory Clocks:** Align infrastructure refresh cycles with national regulatory mandates (e.g., OMB M-23-02, NSA CNSA 2.0, ANSSI, DORA).
            """)
            
        st.markdown("""
        #### 2. NIST Standardized Algorithm Portfolio
        *   **Key Establishment:** **ML-KEM (FIPS 203)** — Module-Lattice Key Encapsulation Mechanism.
        *   **Digital Signatures:** **ML-DSA (FIPS 204)** — Module-Lattice Digital Signature Algorithm.
        *   **Stateless Backup Signatures:** **SLH-DSA (FIPS 205)** — Stateless Hash-Based Signature.
        *   **Compact Signatures:** **FN-DSA (FIPS 206)** — Fast-Fourier Lattice Signature.
        """)
        
    with c_p2:
        st.markdown("""
        #### 3. Regulatory Alignment & National Clocks
        *   **US Federal & Defense:** **OMB M-23-02** (Annual CBOM submissions) & **NSA CNSA 2.0** (2025–2030 transition targets for National Security Systems).
        *   **European Union:** **ANSSI Guidelines** (Mandatory hybridisation default) & **DORA** (ICT cryptographic resilience for financial entities).
        *   **UK NCSC Milestones:** 2028 discovery milestone & phased PQC cutover.
        
        #### 4. Cryptographic Agility Architecture
        *   **Protocol Agility:** Configure TLS 1.3, VPN, and SSH gateways to support dual-stack negotiation and enforce explicit deprecation dates for classical-only cipher suites.
        *   **Symmetric Security Note:** Quantum threats to symmetric encryption (Grover's algorithm) require key expansion to **AES-256** and **SHA-384/512** (not protocol replacement). Note: Legacy SHA-1 represents a classical collision vulnerability.
        """)



# Footer
st.markdown("---")
st.caption("© 2026 RHBSciAdvisory GmbH | Quantum Strategy & Cryptographic Risk Advisory Suite")
