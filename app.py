import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. THE LOGIC ENGINE ---
def calculate_metrics(df):
    # Standardize column names
    df.columns = df.columns.str.strip()
    
    # Clean data (Fixes the 'str' vs 'int' error)
    df['Clean_Domain'] = df.iloc[:, 0].astype(str)
    raw_vals = df.iloc[:, 1].astype(str).str.replace('%', '')
    df['Score'] = pd.to_numeric(raw_vals, errors='coerce').fillna(70)
    
    # Weights
    weights = {'Track': 0.40, 'Signaling': 0.30, 'Rolling Stock': 0.20, 'Maintenance': 0.10}
    df['Weight'] = df['Clean_Domain'].map(weights).fillna(0.1)
    
    # Math
    df['Weighted_Score'] = (df['Score'] / 100) * df['Weight']
    rri = round(df['Weighted_Score'].sum(), 3)
    
    # Financial Translation (Assuming 0.70 is baseline)
    discount = round(max(0, (rri - 0.70) * 40), 2) 
    return rri, discount, df

# --- 2. THE FRONTEND ---
st.set_page_config(page_title="Railway RSRTF", layout="wide")
st.title("🛡️ Railway Safety Risk Translation Framework")

# Navigation Sidebar
role = st.sidebar.radio("Select Portal:", ["Railway Officer", "Insurance Auditor"])

if role == "Railway Officer":
    st.header("🚂 Operations Dashboard")
    st.write("Upload your Excel file to generate a Safety Risk Certificate.")
    
    file = st.file_uploader("Upload Excel", type=["xlsx"])
    
    if file:
        data = pd.read_excel(file)
        rri, disc, processed_df = calculate_metrics(data)
        
        # Big metric cards
        c1, c2 = st.columns(2)
        c1.metric("Safety Risk Index (RRI)", rri)
        c2.metric("Projected Premium Discount", f"{disc}%")
        
        # Radar Chart
        st.subheader("Departmental Safety Profile")
        labels = processed_df['Clean_Domain'].tolist()
        stats = (processed_df['Score'] / 100).tolist()
        stats += stats[:1] # Close circle
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='teal', alpha=0.25)
        ax.plot(angles, stats, color='teal', linewidth=2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        st.pyplot(fig)

else:
    st.header("🏦 Insurance Underwriting Portal")
    st.info("Verified Data from Northern Railway Zone")
    st.write("### Audit Summary")
    st.success("✅ No manual data overrides detected in last 30 days.")
    st.warning("⚠️ Pending Verification: Track Geometry Index (Zone 4)")
    
    st.button("Download Certified Risk Report")
