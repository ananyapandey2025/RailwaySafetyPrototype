import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- LOGIC ENGINE ---
def calculate_metrics(df):
    df.columns = df.columns.str.strip()
    df['Clean_Domain'] = df.iloc[:, 0].astype(str)
    raw_vals = df.iloc[:, 1].astype(str).str.replace('%', '')
    df['Score'] = pd.to_numeric(raw_vals, errors='coerce').fillna(70)
    
    weights = {'Track': 0.40, 'Signaling': 0.30, 'Rolling Stock': 0.20, 'Maintenance': 0.10}
    df['Weight'] = df['Clean_Domain'].map(weights).fillna(0.1)
    df['Weighted_Score'] = (df['Score'] / 100) * df['Weight']
    rri = round(df['Weighted_Score'].sum(), 3)
    
    # Financial translation
    discount = round(max(0, (rri - 0.70) * 40), 2) 
    return rri, discount, df

# --- FRONTEND ---
st.set_page_config(page_title="RSRTF Pro", layout="wide")

# Sidebar
st.sidebar.title("🛡️ RSRTF v2.0")
role = st.sidebar.selectbox("Access Level:", ["🚂 Railway Operations", "🏦 Insurance Underwriting"])

if role == "🚂 Railway Operations":
    st.header("Railway Safety Submission Portal")
    uploaded_file = st.file_uploader("Upload TMS/S&T Performance Data", type=["xlsx"])
    
    if uploaded_file:
        rri, disc, processed_df = calculate_metrics(pd.read_excel(uploaded_file))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Safety Index (RRI)", rri)
        col2.metric("Target Discount", f"{disc}%")
        col3.metric("Status", "Pending Review", delta_color="off")

        # Interactive Chart
        st.subheader("Asset Health Radar")
        labels = processed_df['Clean_Domain'].tolist()
        stats = (processed_df['Score'] / 100).tolist()
        stats += stats[:1]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='green', alpha=0.3)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        st.pyplot(fig)

# --- ENHANCED INSURER SECTION ---
else:
    st.header("🏦 Underwriter Audit & Approval Portal")
    st.markdown("---")
    
    # 1. Verification Checklist (Interactive)
    st.subheader("Data Verification Checklist")
    c1, c2, c3 = st.columns(3)
    v1 = c1.checkbox("Verify IoT Sensor Logs", value=True)
    v2 = c2.checkbox("Cross-check Maintenance Invoices", value=False)
    v3 = c3.checkbox("Validate 3rd Party Safety Audit", value=True)

    # 2. Historical Trend Simulation
    st.subheader("Historical Risk Comparison")
    hist_data = pd.DataFrame({
        'Month': ['Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
        'Historical Avg': [0.72, 0.73, 0.71, 0.74, 0.75],
        'Current Zone Performance': [0.70, 0.75, 0.78, 0.81, 0.86]
    })
    st.line_chart
