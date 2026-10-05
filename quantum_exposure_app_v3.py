import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import json

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
        background-color: #fff9db;
        border-left-color: #f0ad4e;
        color: #856404;
    }
    .low {
        background-color: #ebfbee;
        border-left-color: #5cb85c;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("🔒 Quantum Cryptographic Exposure Analyzer")
st.caption("Interactive Mosca's Theorem Risk Modeler | RHBSciAdvisory GmbH Enterprise Advisory Suite")

st.markdown("""
This web application evaluates organizational exposure to **Harvest Now, Decrypt Later (HNDL)** quantum threats 
using **Mosca's Theorem** ($y + x > z$).
""")

# Sidebar Controls
st.sidebar.image("https://img.icons8.com/color/96/shield-against-piracy.png", width=64)
st.sidebar.title("⚙️ Simulation Controls")

st.sidebar.markdown("### Global Parameter")
z = st.sidebar.slider(
    "Threat Horizon (z) — Years until CRQC:",
    min_value=1,
    max_value=30,
    value=12,
    help="Timeline until a Cryptographically Relevant Quantum Computer (CRQC) capable of breaking RSA-2048 emerges (industry consensus: ~10-15 years)."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Custom Enterprise Parameters")
custom_name = st.sidebar.text_input("Client Organization / Sector Name:", "Custom Enterprise")
y = st.sidebar.slider(
    "Confidentiality Span (y) — Years data must stay secret:",
    min_value=1,
    max_value=100,
    value=15,
    help="How long encrypted records must remain secure from creation date due to compliance, privacy, or trade secret rules."
)
x = st.sidebar.slider(
    "Migration Timeline (x) — Years to deploy PQC:",
    min_value=1,
    max_value=20,
    value=5,
    help="Time required to audit software assets, catalog dependencies in a CBOM, and refactor systems to Post-Quantum Cryptography (PQC)."
)

# Standard Industry Data
default_data = [
    {
        "Client Sector": "Public Research Hospital",
        "Confidentiality Span (y)": 50,
        "Migration Timeline (x)": 6,
        "Description": "Medical health records & genomic IP (50-yr statutory protection)"
    },
    {
        "Client Sector": "Tier-1 Retail Bank",
        "Confidentiality Span (y)": 25,
        "Migration Timeline (x)": 8,
        "Description": "Core banking ledger, SWIFT transactions & wire encryption"
    },
    {
        "Client Sector": "Municipal Government",
        "Confidentiality Span (y)": 10,
        "Migration Timeline (x)": 5,
        "Description": "Citizen registries & tax infrastructure"
    },
    {
        "Client Sector": "E-Commerce Retailer",
        "Confidentiality Span (y)": 3,
        "Migration Timeline (x)": 2,
        "Description": "Session logs & temporary payment tokens"
    }
]

# Add Custom Entry
all_sectors = default_data.copy()
all_sectors.insert(0, {
    "Client Sector": f"*{custom_name} (Custom)*",
    "Confidentiality Span (y)": y,
    "Migration Timeline (x)": x,
    "Description": "User-defined custom parameters"
})

df = pd.DataFrame(all_sectors)
df["Threat Horizon (z)"] = z
df["Total Target Span (y + x)"] = df["Confidentiality Span (y)"] + df["Migration Timeline (x)"]
df["Exposure Deficit"] = df["Total Target Span (y + x)"] - df["Threat Horizon (z)"]

# Risk Calculation
conditions = [
    (df["Exposure Deficit"] > 10),
    (df["Exposure Deficit"] > 0) & (df["Exposure Deficit"] <= 10),
    (df["Exposure Deficit"] <= 0)
]
risk_levels = ["CRITICAL", "HIGH", "LOW"]
df["Risk Level"] = np.select(conditions, risk_levels, default="LOW")

# Main Dashboard Navigation
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Dashboard", 
    "🗺️ Interactive Risk Map", 
    "📋 PQC & CBOM Action Plan", 
    
])

# TAB 1: EXECUTIVE DASHBOARD
with tab1:
    st.markdown("### 🔑 Executive Summary KPI Cards")
    
    # Custom Org Metrics
    custom_row = df.iloc[0]
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.metric(label="Target Span (y + x)", value=f"{custom_row['Total Target Span (y + x)']} yrs")
    with m_col2:
        st.metric(label="Threat Horizon (z)", value=f"{z} yrs")
    with m_col3:
        deficit_val = custom_row['Exposure Deficit']
        delta_str = f"+{deficit_val} yrs deficit" if deficit_val > 0 else f"{deficit_val} yrs safe"
        st.metric(label="Exposure Deficit", value=f"{abs(deficit_val)} yrs", delta=delta_str, delta_color="inverse")
    with m_col4:
        r_level = custom_row['Risk Level']
        st.metric(label="Calculated Risk Tier", value=r_level)

    st.markdown("---")
    st.markdown("### 🏛️ Industry Sector Exposure Matrix")
    
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        # Styled Sector Cards
        for _, row in df.iterrows():
            s_name = row["Client Sector"]
            s_y = row["Confidentiality Span (y)"]
            s_x = row["Migration Timeline (x)"]
            s_span = row["Total Target Span (y + x)"]
            s_deficit = row["Exposure Deficit"]
            s_risk = row["Risk Level"]
            
            if s_risk == "CRITICAL":
                c_class = "critical"
                s_msg = f"🚨 **CRITICAL DEFICIT (+{s_deficit} yrs):** Encrypted data intercepted today is vulnerable to retroactive decryption before PQC migration completes."
            elif s_risk == "HIGH":
                c_class = "high"
                s_msg = f"⚠️ **HIGH RISK (+{s_deficit} yrs):** Narrow security margin. Accelerated CBOM auditing required."
            else:
                c_class = "low"
                s_msg = f"✅ **SECURE MARGIN ({abs(s_deficit)} yrs safe):** System security span is within the quantum threat horizon."
                
            st.markdown(f"""
                <div class='report-card {c_class}'>
                    <h4 style='margin-bottom:4px;'>{s_name}</h4>
                    <p style='margin-bottom:6px;'><b>Confidentiality (y):</b> {s_y} yrs | <b>Migration (x):</b> {s_x} yrs | <b>Total (y+x):</b> {s_span} yrs</p>
                    <p style='margin-bottom:0px;'>{s_msg}</p>
                </div>
         """, unsafe_allow_html=True)
            
    with col_b:
        st.markdown("#### 📥 Export Assessment")
        st.dataframe(df[["Client Sector", "Confidentiality Span (y)", "Migration Timeline (x)", "Exposure Deficit", "Risk Level"]], use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Assessment Data (CSV)",
            data=csv,
            file_name="quantum_exposure_assessment.csv",
            mime="text/csv",
            use_container_width=True
        )

# TAB 2: INTERACTIVE RISK MAP
with tab2:
    st.markdown("### 🗺️ Interactive Plotly Mosca Boundary Map")
    st.caption("Hover over data points to inspect individual sector coordinates and risk zones.")
    
    # Plotly Interactive Figure
    fig = go.Figure()
    
    # Add Security Boundary Line (y + x = z)
    x_line = np.linspace(0, 15, 100)
    y_line = np.clip(z - x_line, 0, 100)
    
    fig.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode='lines',
        name=f'Security Boundary (y + x = {z})',
        line=dict(color='#343a40', width=2, dash='dash')
    ))
    
    # Add Color-Coded Scatter Points
    color_map = {"CRITICAL": "#d9534f", "HIGH": "#f0ad4e", "LOW": "#5cb85c"}
    
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Migration Timeline (x)"]],
            y=[row["Confidentiality Span (y)"]],
            mode='markers+text',
            name=row["Client Sector"].replace("*", ""),
            text=[row["Client Sector"].replace("*", "")],
            textposition="top right",
            marker=dict(
                size=16,
                color=color_map[row["Risk Level"]],
                line=dict(width=2, color='DarkSlateGrey')
            ),
            hovertemplate=(
                f"<b>{row['Client Sector']}</b><br>" +
                f"Confidentiality Span (y): {row['Confidentiality Span (y)']} yrs<br>" +
                f"Migration Time (x): {row['Migration Timeline (x)']} yrs<br>" +
                f"Total Target Span (y+x): {row['Total Target Span (y + x)']} yrs<br>" +
                f"Risk Status: <b>{row['Risk Level']}</b><extra></extra>"
            )
        ))
        
    fig.update_layout(
        title=dict(text=f"Mosca's Theorem Security Regions (Threat Horizon z = {z} Years)", font=dict(size=16)),
        xaxis_title="Migration Timeline in Years (x)",
        yaxis_title="Data Secrecy Lifespan in Years (y)",
        xaxis=dict(range=[0, 15], gridcolor="#e9ecef"),
        yaxis=dict(range=[0, 60], gridcolor="#e9ecef"),
        template="plotly_white",
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: PQC & CBOM ACTION PLAN
with tab3:
    st.markdown("### 🛡️ Recommended Post-Quantum Remediation Framework")
    
    c_p1, c_p2 = st.columns(2)
    
    with c_p1:
        st.markdown("""
        #### 1. Automated CBOM Discovery (Immediate)
        *   **Catalog Cryptographic Assets:** Deploy static application security testing (SAST) scripts to identify RSA, ECC, Diffie-Hellman, and SHA-1 instances across codebases.
        *   **Export Machine-Readable CBOM:** Generate JSON/CSV inventories tracking algorithms, key lengths, and supplier origins.
        
        #### 2. NIST Standard Adoption (Years 1–3)
        *   **Key Encapsulation:** Replace RSA/ECC key exchanges with **ML-KEM (FIPS 203 / CRYSTALS-Kyber)** to defend against HNDL attacks.
        *   **Digital Signatures:** Migrate authentication to **ML-DSA (FIPS 204)** and **SLH-DSA (FIPS 205)**.
        """)
        
    with c_p2:
        st.markdown("""
        #### 3. Hybrid Cryptographic Deployments
        *   **Dual-Wrapped Protocols:** Combine classical algorithms (e.g., X25519) with PQC wrappers to maintain compliance while testing quantum resilience.
        *   **Crypto-Agility:** Refactor security architectures into modular components that permit algorithm swapping without rewriting core business logic.
        
        #### 4. Supply Chain Governance
        *   **Vendor Mandates:** Require third-party SaaS/PaaS vendors to disclose CBOM inventories and commit to NIST 2030/2035 deprecation roadmaps.
        """)



# Footer
st.markdown("---")
st.caption("© 2026 RHBSciAdvisory GmbH | Quantum Strategy & Cryptographic Risk Advisory Suite")
