import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import base64
import json

# Set up page config
st.set_page_config(
    page_title="RHBSciAdvisory | Quantum Risk & Exposure Analyzer",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling & Theme
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #0b1a30;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        text-align: center;
    }
    .report-card {
        padding: 16px;
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
    .thin-slack {
        background-color: #e2f0d9;
        border-left-color: #8cbf26;
        color: #2e5109;
    }
    .secure {
        background-color: #ebfbee;
        border-left-color: #5cb85c;
        color: #155724;
    }
    .param-upgrade {
        background-color: #e6f2ff;
        border-left-color: #0275d8;
        color: #004085;
    }
    .refused-banner {
        background-color: #721c24;
        color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 16px;
    }
    .approved-banner {
        background-color: #155724;
        color: #ffffff;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("🔒 Enterprise Quantum Cryptographic Risk & Exposure Analyzer")
st.caption("Audited Mosca's Theorem Risk Engine ($x + y > z$) | Loredo Risk Tiers | RHBSciAdvisory GmbH Suite")

# Governance Disclaimer Banner
st.info(
    "🏛️ **Governance Notice:** This analyzer evaluates organizational exposure using Mosca's timing predicate ($x + y > z$), "
    "where $x$ is Confidentiality Span / Shelf-Life, $y$ is Migration Timeline, and $z$ is the CRQC Threat Horizon. "
    "In accordance with CQO Handbook governance standards, **no single aggregate readiness score is emitted**; "
    "readiness is evaluated strictly per domain and per asset."
)

# Sidebar Controls & Global Threat Horizon (z)
st.sidebar.title("⚙️ Global Horizon & Controls")
st.sidebar.markdown("### Threat Horizon ($z$) Scenario")

z_scenario = st.sidebar.radio(
    "Select Threat Horizon ($z$) Model:",
    ["Central Consensus (z = 12 yrs)", "Aggressive CRQC (z = 8 yrs)", "Conservative (z = 20 yrs)", "Custom Slider"],
    index=0,
    help="Timeline until a Cryptographically Relevant Quantum Computer (CRQC) capable of breaking RSA/ECC emerges."
)

if z_scenario == "Central Consensus (z = 12 yrs)":
    z_val = 12
elif z_scenario == "Aggressive CRQC (z = 8 yrs)":
    z_val = 8
elif z_scenario == "Conservative (z = 20 yrs)":
    z_val = 20
else:
    z_val = st.sidebar.slider(
        "Threat Horizon ($z$) in Years:",
        min_value=0,
        max_value=30,
        value=12,
        help="Global threat horizon z (Mosca collapse time)."
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏛️ CQO Governance Rules")
st.sidebar.markdown("""
- **Single Intake Door:** CQO holds vendor intake.
- **CISO Boundary Split:** CISO owns operational cybersecurity & PKI build; CQO owns strategy & board translation.
- **Year-1 Policy:** No on-premises QPU purchases.
- **PoC Refusal Rule:** Compute PoCs are REFUSED if Security bucket has unowned exposure deficits or hard gates fail.
- **No Single Readiness Score:** Evaluated per domain.
""")

# Standard Default Enterprise Asset Inventory (Replacing single org sliders with asset rows)
default_assets = [
    {
        "asset_name": "Core Banking Payment Gateway TLS",
        "primitive": "Asymmetric Key Exchange (RSA/ECC)",
        "use": "External Partner & Transaction Key Exchange",
        "shelf_life_x": 15,
        "migration_y": 5,
        "owner": "Jane Doe (CISO Security Lead)",
        "bucket": "Security",
        "loredo_tier": "Tier 1: Foundational / Priority Wave 1",
        "gate1_formulation": True,
        "gate2_baseline": True,
        "gate3_owner": True
    },
    {
        "asset_name": "EHR Patient Medical Records Archive",
        "primitive": "Asymmetric Key Exchange (RSA-2048)",
        "use": "Statutory Patient Health Data Protection",
        "shelf_life_x": 50,
        "migration_y": 6,
        "owner": "Unassigned",
        "bucket": "Security",
        "loredo_tier": "Tier 1: Foundational / Priority Wave 1",
        "gate1_formulation": True,
        "gate2_baseline": True,
        "gate3_owner": False
    },
    {
        "asset_name": "Software Firmware Update Signing Key",
        "primitive": "Digital Signature (ECDSA)",
        "use": "Code Signing & Infrastructure Identity",
        "shelf_life_x": 10,
        "migration_y": 5,
        "owner": "Robert Smith (DevOps Lead)",
        "bucket": "Security",
        "loredo_tier": "Tier 1: Foundational / Priority Wave 1",
        "gate1_formulation": True,
        "gate2_baseline": True,
        "gate3_owner": True
    },
    {
        "asset_name": "Customer Database At-Rest Encryption",
        "primitive": "Symmetric Cipher (AES-128)",
        "use": "At-Rest Database Table Encryption",
        "shelf_life_x": 10,
        "migration_y": 3,
        "owner": "Data Engineering Lead",
        "bucket": "Security",
        "loredo_tier": "Tier 2: Quantum-Adjacent / Wave 3 Refresh",
        "gate1_formulation": True,
        "gate2_baseline": True,
        "gate3_owner": True
    },
    {
        "asset_name": "Legacy Password Hash Verification",
        "primitive": "Hash Function (SHA-1)",
        "use": "Legacy User Authentication Service",
        "shelf_life_x": 2,
        "migration_y": 2,
        "owner": "IAM Operations Team",
        "bucket": "Security",
        "loredo_tier": "Tier 2: Quantum-Adjacent / Wave 3 Refresh",
        "gate1_formulation": True,
        "gate2_baseline": True,
        "gate3_owner": True
    },
    {
        "asset_name": "Financial Portfolio Deep Hedging Engine",
        "primitive": "Quantum Optimization Kernel (VQE/QAOA)",
        "use": "Multi-Period Risk & Collateral Optimization",
        "shelf_life_x": 2,
        "migration_y": 2,
        "owner": "Head of Quantitative Research",
        "bucket": "Optimization",
        "loredo_tier": "Tier 2: Quantum-Adjacent / Mid-Term Option",
        "gate1_formulation": True,
        "gate2_baseline": True,
        "gate3_owner": True
    }
]

# Section for Adding / Modifying Asset Rows
st.markdown("### 📝 Asset-Level Risk Inventory Input")
st.caption("Each row represents a specific cryptographic asset or compute candidate. Modify parameters directly in the table or sidebar.")

# Initialize Session State for Assets
if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = pd.DataFrame(default_assets)

# Expander for Adding a New Asset Row
with st.expander("➕ Add New Cryptographic Asset or Compute Candidate", expanded=False):
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1:
        new_name = st.text_input("Asset / Candidate Name:", "New System Asset")
        new_primitive = st.selectbox(
            "Primitive:",
            [
                "Asymmetric Key Exchange (RSA/ECC)",
                "Digital Signature (RSA/ECDSA)",
                "Symmetric Cipher (AES-128)",
                "Symmetric Cipher (AES-256)",
                "Hash Function (SHA-1)",
                "Hash Function (SHA-256/384)",
                "Quantum Optimization Kernel (VQE/QAOA)",
                "Quantum Molecular Simulation"
            ]
        )
    with col_i2:
        new_use = st.text_input("Specific Business Use:", "Production Service")
        new_bucket = st.selectbox("4-Bucket Taxonomy:", ["Security", "Optimization", "Simulation", "Machine Learning"])
    with col_i3:
        new_x = st.number_input("Shelf-Life $x$ (Years):", min_value=0, max_value=100, value=10, help="Confidentiality span x.")
        new_y = st.number_input("Migration Time $y$ (Years):", min_value=0, max_value=30, value=4, help="Migration timeline y.")
    with col_i4:
        new_owner = st.text_input("Named Owner:", "Unassigned")
        new_tier = st.selectbox(
            "Loredo Tier:",
            [
                "Tier 1: Foundational / Priority Wave 1",
                "Tier 2: Quantum-Adjacent / Wave 3 Refresh",
                "Tier 3: Deep Specialization / Long-Term"
            ]
        )
    
    col_g1, col_g2, col_g3, col_btn = st.columns([1, 1, 1, 1])
    with col_g1:
        new_g1 = st.checkbox("Gate 1: Formulated on 1 page?", value=True)
    with col_g2:
        new_g2 = st.checkbox("Gate 2: Strong classical baseline?", value=True)
    with col_g3:
        new_g3 = st.checkbox("Gate 3: Named outcome owner?", value=True)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Row to Inventory"):
            new_row = {
                "asset_name": new_name,
                "primitive": new_primitive,
                "use": new_use,
                "shelf_life_x": new_x,
                "migration_y": new_y,
                "owner": new_owner,
                "bucket": new_bucket,
                "loredo_tier": new_tier,
                "gate1_formulation": new_g1,
                "gate2_baseline": new_g2,
                "gate3_owner": new_g3
            }
            st.session_state.inventory_df = pd.concat([st.session_state.inventory_df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Added '{new_name}' to inventory!")
            st.rerun()

# Process Inventory Data & Calculate Mosca's Letters
df = st.session_state.inventory_df.copy()
df["z_horizon"] = z_val
df["target_span_xy"] = df["shelf_life_x"] + df["migration_y"]
df["signed_slack_s"] = df["z_horizon"] - df["target_span_xy"]
df["exposure_deficit_d"] = df["target_span_xy"] - df["z_horizon"]
df["mosca_predicate"] = df["target_span_xy"] > df["z_horizon"]

# Classify Risk Status per Row
def evaluate_row_risk(row):
    bucket = row["bucket"]
    primitive = row["primitive"]
    deficit = row["exposure_deficit_d"]
    slack = row["signed_slack_s"]
    
    if bucket == "Security":
        if "AES-256" in primitive or "SHA-256/384" in primitive:
            return "SAFE / PARAMETER ADEQUATE"
        elif "AES-128" in primitive:
            return "TIER 2 PARAMETER UPGRADE"
        elif "SHA-1" in primitive:
            return "CLASSICAL HYGIENE DEPRECATION"
        else:
            if deficit > 10:
                return "CRITICAL EXPOSURE DEFICIT"
            elif deficit > 0:
                return "HIGH EXPOSURE DEFICIT"
            elif slack <= 5:
                return "THIN SECURITY SLACK"
            else:
                return "SECURE MARGIN"
    else:
        # Compute candidates
        if not (row["gate1_formulation"] and row["gate2_baseline"] and row["gate3_owner"]):
            return "HARD GATE FAILED"
        else:
            return "COMPUTE POC EVALUATION"

df["eval_status"] = df.apply(evaluate_row_risk, axis=1)

# Check Refusal Rule for Compute Proofs of Concept
# Rule: Refuse a compute proof of concept while security bucket has an open deficit AND no owner (or unassigned owner), or if hard gates fail.
security_unowned_deficits = df[
    (df["bucket"] == "Security") & 
    (df["exposure_deficit_d"] > 0) & 
    (df["owner"].str.lower().str.contains("unassigned|none|^$"))
]

has_open_unowned_security_deficit = len(security_unowned_deficits) > 0

# Overall Compute PoC Authorization Decision
compute_poc_refused = has_open_unowned_security_deficit

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Asset Dashboard",
    "🗺️ Mosca Security Boundary Map",
    "🛡️ Tier Remediation & Refusal Rules",
    "🏛️ Mandate & CISO Boundary Export"
])

# TAB 1: EXECUTIVE ASSET DASHBOARD
with tab1:
    st.markdown("### 🔑 Executive Summary KPI Metrics")
    
    total_assets = len(df)
    sec_assets = len(df[df["bucket"] == "Security"])
    sec_deficits = len(df[(df["bucket"] == "Security") & (df["mosca_predicate"] == True)])
    unowned_sec_deficits = len(security_unowned_deficits)
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="Total Inventoried Assets", value=total_assets)
    with k2:
        st.metric(label="Security Surfaces", value=sec_assets)
    with k3:
        st.metric(label="Open Security Deficits ($x+y > z$)", value=sec_deficits, delta=f"{sec_deficits} vulnerable", delta_color="inverse")
    with k4:
        st.metric(label="Unowned Security Deficits", value=unowned_sec_deficits, delta="Refusal Trigger!" if unowned_sec_deficits > 0 else "0 Unowned", delta_color="inverse")

    # Compute PoC Status Banner
    st.markdown("---")
    st.markdown("### 🛑 Governance Refusal Gate Status")
    
    if compute_poc_refused:
        st.markdown(f"""
            <div class='refused-banner'>
                ⛔ <b>COMPUTE PROOF-OF-CONCEPT REFUSED!</b><br>
                Governance Rule Triggered: Compute PoCs (Optimization/Simulation/ML) CANNOT be funded or executed while 
                the Security bucket has <b>{unowned_sec_deficits} unowned asset(s)</b> with an active exposure deficit ($x + y > z$).<br>
                <i>Action Required: Assign a named security owner to all vulnerable cryptographic surfaces before requesting compute budget.</i>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='approved-banner'>
                ✅ <b>COMPUTE PROOF-OF-CONCEPT GATE ELIGIBLE:</b><br>
                All Security bucket exposure deficits have assigned outcome owners. Compute candidates meeting the 3 Hard Gates may proceed to Council review.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Asset-Level Exposure & Mosca Parameters")
    
    # Display Table with Explicit Columns
    disp_cols = [
        "asset_name", "bucket", "primitive", "shelf_life_x", "migration_y", 
        "target_span_xy", "z_horizon", "signed_slack_s", "exposure_deficit_d", 
        "owner", "loredo_tier", "eval_status"
    ]
    
    disp_df = df[disp_cols].copy()
    disp_df.columns = [
        "Asset Name", "Bucket", "Primitive", "Shelf-Life ($x$)", "Migration ($y$)", 
        "Target ($x+y$)", "Horizon ($z$)", "Slack ($s$)", "Deficit ($d$)", 
        "Owner", "Loredo Tier", "Status"
    ]
    
    st.dataframe(disp_df, use_container_width=True)

# TAB 2: MOSCA SECURITY BOUNDARY MAP
with tab2:
    st.markdown("### 🗺️ Mosca Security Boundary Map ($x + y = z$)")
    st.caption("Plotting Confidentiality Span ($x$) vs Migration Time ($y$). Assets above the dashed boundary line represent active HNDL exposure deficits.")
    
    fig = go.Figure()
    
    # Add Security Boundary Line (x + y = z)
    x_range = np.linspace(0, 60, 100)
    y_bound = np.clip(z_val - x_range, 0, 30)
    
    fig.add_trace(go.Scatter(
        x=x_range, y=y_bound,
        mode='lines',
        name=f'Security Boundary (x + y = {z_val} yrs)',
        line=dict(color='#212529', width=2, dash='dash')
    ))
    
    # Color Map for Statuses
    color_map = {
        "CRITICAL EXPOSURE DEFICIT": "#d9534f",
        "HIGH EXPOSURE DEFICIT": "#f0ad4e",
        "THIN SECURITY SLACK": "#8cbf26",
        "SECURE MARGIN": "#5cb85c",
        "TIER 2 PARAMETER UPGRADE": "#0275d8",
        "SAFE / PARAMETER ADEQUATE": "#6c757d",
        "CLASSICAL HYGIENE DEPRECATION": "#17a2b8",
        "HARD GATE FAILED": "#a94442",
        "COMPUTE POC EVALUATION": "#6f42c1"
    }
    
    for _, row in df.iterrows():
        status = row["eval_status"]
        fig.add_trace(go.Scatter(
            x=[row["shelf_life_x"]],
            y=[row["migration_y"]],
            mode='markers+text',
            name=row["asset_name"],
            text=[row["asset_name"]],
            textposition="top right",
            marker=dict(
                size=16,
                color=color_map.get(status, "#000000"),
                line=dict(width=2, color='DarkSlateGrey')
            ),
            hovertemplate=(
                f"<b>{row['asset_name']}</b><br>" +
                f"Primitive: {row['primitive']}<br>" +
                f"Shelf-Life (x): {row['shelf_life_x']} yrs<br>" +
                f"Migration Time (y): {row['migration_y']} yrs<br>" +
                f"Target Span (x+y): {row['target_span_xy']} yrs<br>" +
                f"Signed Slack (s): {row['signed_slack_s']} yrs<br>" +
                f"Deficit (d): {row['exposure_deficit_d']} yrs<br>" +
                f"Owner: {row['owner']}<br>" +
                f"Status: <b>{status}</b><extra></extra>"
            )
        ))
        
    fig.update_layout(
        title=dict(text=f"Mosca's Theorem Security Boundary ($z = {z_val}$ Years)", font=dict(size=16)),
        xaxis_title="Confidentiality Span / Shelf-Life in Years (x)",
        yaxis_title="Migration Timeline in Years (y)",
        xaxis=dict(range=[0, 60], gridcolor="#e9ecef"),
        yaxis=dict(range=[0, 20], gridcolor="#e9ecef"),
        template="plotly_white",
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: TIER REMEDIATION & REFUSAL RULES
with tab3:
    st.markdown("### 🛡️ Primitive & Tier-Driven PQC Remediation Plan")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("""
        #### 🔑 1. Asymmetric Cryptography (Shor Clock Driven)
        * **Key Establishment / Exchange:** Replace RSA / ECDH with **ML-KEM (FIPS 203 / CRYSTALS-Kyber)**.
        * **Digital Signatures & Authentication:** Replace RSA / ECDSA with **ML-DSA (FIPS 204)** or **SLH-DSA (FIPS 205)** for hash-based backup.
        * **Hybrid Transition:** Deploy dual-wrapped classical + PQC cipher suites (e.g., X25519 + ML-KEM-768) to protect data-in-transit today.
        
        #### 🧱 2. Cryptographic Agility Architecture
        * **Abstract Security Service Layer:** Isolate cryptographic primitives behind APIs to enable algorithm swapping without rewriting business applications.
        * **Machine-Readable CBOM:** Export JSON/CSV Cryptographic Bill of Materials detailing algorithms, key lengths, and supplier locations.
        """)
        
    with col_p2:
        st.markdown("""
        #### ⚙️ 3. Cryptographic Truths & Non-Shor Primitives
        * **AES-256 Does NOT Feed the Shor Clock:** AES-256 is symmetric encryption, affected weakly by Grover (halved key to AES-128 equivalent). It remains secure and does not drive post-quantum asymmetric migration.
        * **AES-128 is Tier 2 Parameter Upgrade:** Grover reduces AES-128 to 64-bit security. Upgrade to AES-256 during standard refresh cycles. Not an asymmetric quantum break.
        * **SHA-1 Stays Classical Hygiene:** SHA-1 is broken due to classical collision attacks. Deprecation is classical security hygiene, not a Shor quantum break.
        
        #### ⛔ 4. The Three Hard Gates & Compute Refusal Rule
        1. **Formulation Gate:** Problem objective & constraints written on 1 page.
        2. **Classical Baseline Gate:** Benchmark against the best realistic classical solver.
        3. **Outcome Owner Gate:** Named business outcome owner who signs the decision.
        * **Veto Rule:** Refuse Compute PoCs if Security bucket has unowned deficits or hard gates fail.
        """)

    st.markdown("---")
    st.markdown("### 🔍 Compute Candidates Hard Gate Scorecard")
    
    compute_df = df[df["bucket"] != "Security"].copy()
    if len(compute_df) > 0:
        st.dataframe(compute_df[[
            "asset_name", "bucket", "primitive", "owner", 
            "gate1_formulation", "gate2_baseline", "gate3_owner", "eval_status"
        ]], use_container_width=True)
    else:
        st.info("No compute candidates currently in inventory.")

# TAB 4: MANDATE & CISO BOUNDARY EXPORT
with tab4:
    st.markdown("### 🏛️ Executive Mandate Fields & CISO Boundary Charter")
    
    st.markdown("""
    #### 📜 1. Mandate Charter & Role Allocation
    * **Single Intake Door:** The Chief Quantum Officer (CQO) holds the single intake door for all vendor and research interactions.
    * **CISO Boundary Split:**
      * **CISO / Security Engineering:** Owns operational cybersecurity, PKI operations, certificate issuance, and migration builds.
      * **CQO:** Owns quantum strategy, inventory sponsorship, board translation, and the production gate.
    * **Year-One No On-Prem QPU Policy:** Refuse on-premises quantum hardware/dilution refrigerator purchases in Year 1 in favor of multi-vendor cloud access and classical benchmarking.
    * **No Single Readiness Score:** Enterprise readiness is NEVER compressed into a single composite score. Domain-specific ranks are reported independently.
    """)
    
    st.markdown("---")
    st.markdown("### 📥 Export Full Mandate & Inventory Audit Data")
    
    # Build Export Dataset including Mandate & Boundary Fields
    export_df = df.copy()
    export_df["ciso_boundary_split"] = "CISO: Operations & PKI Build | CQO: Strategy & Board Translation"
    export_df["single_intake_door"] = "Enforced via CQO Office"
    export_df["single_readiness_score_emitted"] = False
    export_df["year1_no_onprem_qpu_policy"] = "Enforced"
    export_df["compute_poc_refusal_active"] = compute_poc_refused
    
    csv_bytes = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📄 Download Complete Mandate Audit & Inventory CSV",
        data=csv_bytes,
        file_name="quantum_exposure_mandate_audit.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.caption("© 2026 RHBSciAdvisory GmbH | Quantum Strategy & Cryptographic Risk Advisory Suite")
