import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingestion.generate_data import generate_patient_records
from ingestion.validate_load import validate_and_load

os.makedirs("data", exist_ok=True)
engine = create_engine("sqlite:///data/health.db")

st.set_page_config(
    page_title="Rural Health Intelligence",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
* { font-family: 'DM Sans', sans-serif; }
.main { background-color: #080c14; }
.block-container { padding-top: 1.5rem; }
.metric-card {
    background: linear-gradient(135deg, #0d1520, #111c2e);
    border-radius: 14px;
    padding: 22px 18px;
    border: 1px solid #1e3050;
    text-align: center;
}
.metric-value { font-size: 2.4rem; font-weight: 700; color: #fff; }
.metric-label { font-size: 0.75rem; color: #5a7a9a;
    text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px; }
.metric-sub { font-size: 0.8rem; color: #2d9cdb; margin-top: 5px; }
.alert-outbreak {
    background: linear-gradient(135deg, #2d0a0a, #3d1010);
    border: 1px solid #ff4444; border-left: 4px solid #ff4444;
    border-radius: 10px; padding: 14px 18px; margin: 6px 0;
    color: #ff8080;
}
.alert-watch {
    background: linear-gradient(135deg, #2d1f00, #3d2a00);
    border: 1px solid #ffaa00; border-left: 4px solid #ffaa00;
    border-radius: 10px; padding: 14px 18px; margin: 6px 0;
    color: #ffd060;
}
.alert-normal {
    background: linear-gradient(135deg, #001f10, #002a18);
    border: 1px solid #00cc66; border-left: 4px solid #00cc66;
    border-radius: 10px; padding: 14px 18px; margin: 6px 0;
    color: #60ffaa;
}
.section-header {
    font-size: 1.1rem; font-weight: 600; color: #fff;
    border-bottom: 2px solid #1e3050;
    padding-bottom: 8px; margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 Health Intelligence")
    st.markdown("---")
    st.markdown("""
    **A data engineering pipeline for rural healthcare monitoring:**
    - Patient data ingestion and validation
    - SQLite data warehouse
    - dbt transformations
    - Disease outbreak detection
    - Health worker performance tracking

    **Stack:** Python SQL dbt Streamlit
    """)
    st.markdown("---")
    st.markdown("### Load Data")
    data_source = st.radio(
        "Choose data source",
        ["Generate Fake Data", "Upload CSV File", "Google Sheets"]
    )

    if data_source == "Generate Fake Data":
        st.markdown("#### Generate Simulated Data")
        n = st.slider("Number of patient records", 100, 1000, 300)
        if st.button("Generate + Load Data", type="primary"):
            with st.spinner("Generating and loading records..."):
                df = generate_patient_records(n)
                validate_and_load(df)
            st.success(f"Loaded {n} records successfully!")
            st.rerun()

    if data_source == "Upload CSV File":
        st.markdown("#### Upload Patient CSV")
        st.caption("CSV must have these columns:")
        st.code("patient_id, name, age, gender, village, visit_date, diagnosis, temperature_c, systolic_bp, diastolic_bp, blood_glucose, referred_to_hospital, health_worker_id, health_worker_name")
        uploaded_file = st.file_uploader(
            "Choose CSV or Excel file",
            type=["csv", "xlsx", "xls"]
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.success(f"File loaded: {len(df)} rows found")
                st.dataframe(df.head(3), use_container_width=True)
                if st.button("Load into Database", type="primary"):
                    with st.spinner("Validating and saving..."):
                        validate_and_load(df)
                    st.success(f"Saved {len(df)} records!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}")

    if data_source == "Google Sheets":
        st.markdown("#### Connect Google Sheets")
        with st.expander("How to set up — click to see steps"):
            st.markdown("**Step 1** — Open your Google Sheet")
            st.markdown("**Step 2** — Click Share button at top right")
            st.markdown("**Step 3** — Click Change to anyone with the link")
            st.markdown("**Step 4** — Set permission to Viewer")
            st.markdown("**Step 5** — Click Copy link")
            st.markdown("**Step 6** — Paste that link below")
            st.markdown("---")
            st.markdown("**Your sheet must have these column names in Row 1:**")
            st.code("patient_id, name, age, gender, village, visit_date, diagnosis, temperature_c, systolic_bp, diastolic_bp, blood_glucose, referred_to_hospital, health_worker_id, health_worker_name")
        sheet_url = st.text_input(
            "Paste your Google Sheet URL",
            placeholder="https://docs.google.com/spreadsheets/d/..."
        )
        if st.button("Fetch from Google Sheets", type="primary"):
            if sheet_url.strip() == "":
                st.warning("Please paste a Google Sheet URL")
            else:
                with st.spinner("Fetching data..."):
                    try:
                        from ingestion.google_sheets import fetch_from_google_sheets
                        df = fetch_from_google_sheets(sheet_url)
                        st.success(f"Fetched {len(df)} rows!")
                        st.dataframe(df.head(3), use_container_width=True)
                        validate_and_load(df)
                        st.success("Saved to database!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

# ── HEADER ─────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='color:white; font-size:2rem; margin-bottom:4px;'>
🏥 Rural Health Intelligence Pipeline
</h1>
<p style='color:#5a7a9a; margin-bottom:24px;'>
Community health worker performance and disease surveillance dashboard
</p>
""", unsafe_allow_html=True)

# ── HOW TO ADD DATA GUIDE ──────────────────────────────────────────────────
with st.expander("ℹ️ How to add your own data — click to see 3 ways"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 📊 Way 1 — CSV File
        1. Download our template from GitHub
        2. Fill in your patient data
        3. Go to sidebar
        4. Select Upload CSV File
        5. Upload your file
        6. Click Load into Database
        """)
    with col2:
        st.markdown("""
        ### 📝 Way 2 — Google Sheets
        1. Open your Google Sheet
        2. Click Share at top right
        3. Set to Anyone with link
        4. Set permission to Viewer
        5. Copy the link
        6. Paste in sidebar
        7. Click Fetch from Google Sheets
        """)
    with col3:
        st.markdown("""
        ### 🤖 Way 3 — Generate Test Data
        1. Go to sidebar
        2. Select Generate Fake Data
        3. Choose number of records
        4. Click Generate and Load Data
        5. Dashboard updates instantly
        6. Use this for testing only
        """)
    st.info("For real use, upload a CSV or connect Google Sheets with actual patient visit records collected by health workers.")

# ── CHECK DATA EXISTS ──────────────────────────────────────────────────────
try:
    total = pd.read_sql(
        "SELECT COUNT(*) as c FROM raw_patients", engine).iloc[0]['c']
    if total == 0:
        st.info("No data yet. Click Generate + Load Data in the sidebar to get started.")
        st.stop()
except Exception:
    st.info("No data yet. Click Generate + Load Data in the sidebar to get started.")
    st.stop()

# ── TOP METRICS ────────────────────────────────────────────────────────────
villages  = pd.read_sql("SELECT COUNT(DISTINCT village) as c FROM raw_patients", engine).iloc[0]['c']
workers   = pd.read_sql("SELECT COUNT(DISTINCT health_worker_id) as c FROM raw_patients", engine).iloc[0]['c']
referred  = pd.read_sql("SELECT COUNT(*) as c FROM raw_patients WHERE referred_to_hospital=1", engine).iloc[0]['c']
outbreaks = pd.read_sql("SELECT COUNT(*) as c FROM raw_patients WHERE temperature_c > 38.5", engine).iloc[0]['c']

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    (c1, "👥", total,     "#2d9cdb", "Total Patients",     "All records"),
    (c2, "🏘️", villages,  "#27ae60", "Villages Covered",   "Across regions"),
    (c3, "👩‍⚕️", workers,   "#9b59b6", "Health Workers",     "Active CHWs"),
    (c4, "🏨", referred,  "#e74c3c", "Hospital Referrals", "Sent to hospital"),
    (c5, "🌡️", outbreaks, "#f39c12", "Fever Cases",        "Temp above 38.5C"),
]
for col, icon, val, color, label, sub in metrics:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size:1.8rem'>{icon}</div>
            <div class='metric-value' style='color:{color}'>{val}</div>
            <div class='metric-label'>{label}</div>
            <div class='metric-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚨 Outbreak Alerts",
    "👩‍⚕️ Worker Performance",
    "🏘️ Village Health",
    "📊 Disease Trends",
    "👶 Vulnerable Groups"
])

# ── TAB 1: OUTBREAK ALERTS ─────────────────────────────────────────────────
with tab1:
    st.markdown("<div class='section-header'>Disease Outbreak Surveillance</div>", unsafe_allow_html=True)
    alerts_df = pd.read_sql("""
        SELECT diagnosis, village, COUNT(*) as cases,
            ROUND(AVG(temperature_c),1) as avg_temp,
            SUM(referred_to_hospital) as referrals
        FROM raw_patients
        GROUP BY diagnosis, village
        ORDER BY cases DESC LIMIT 30
    """, engine)

    for _, row in alerts_df.iterrows():
        if row['cases'] >= 20:
            css, icon, level = "alert-outbreak", "🚨", "OUTBREAK ALERT"
        elif row['cases'] >= 10:
            css, icon, level = "alert-watch", "⚠️", "WATCH"
        else:
            css, icon, level = "alert-normal", "✅", "NORMAL"
        st.markdown(f"""
        <div class='{css}'>
            {icon} <b>{level}</b> &nbsp;|&nbsp;
            <b>{row['diagnosis']}</b> in <b>{row['village']}</b>
            &nbsp;|&nbsp; Cases: <b>{row['cases']}</b>
            &nbsp;|&nbsp; Avg Temp: <b>{row['avg_temp']}C</b>
            &nbsp;|&nbsp; Referrals: <b>{int(row['referrals'])}</b>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig = px.treemap(alerts_df, path=['village', 'diagnosis'],
                     values='cases', color='cases',
                     color_continuous_scale='Reds',
                     title="Disease Cases by Village",
                     template="plotly_dark")
    fig.update_layout(paper_bgcolor="#0d1520")
    st.plotly_chart(fig, use_container_width=True)

# ── TAB 2: WORKER PERFORMANCE ──────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-header'>Health Worker Performance Tracker</div>", unsafe_allow_html=True)
    worker_df = pd.read_sql("""
        SELECT health_worker_name, health_worker_id,
            COUNT(*) as total_visits,
            COUNT(DISTINCT village) as villages_covered,
            COUNT(DISTINCT diagnosis) as diseases_handled,
            SUM(referred_to_hospital) as referrals,
            SUM(is_child_under_5) as child_visits,
            SUM(is_elderly) as elderly_visits,
            ROUND(100.0*SUM(referred_to_hospital)/COUNT(*),1) as referral_pct
        FROM raw_patients
        GROUP BY health_worker_id, health_worker_name
        ORDER BY total_visits DESC
    """, engine)

    st.dataframe(worker_df, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.bar(worker_df, x='health_worker_name',
                      y='total_visits', color='villages_covered',
                      title="Total Visits per Health Worker",
                      template="plotly_dark",
                      color_continuous_scale='Blues')
        fig2.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520", xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig3 = px.scatter(worker_df,
                          x='total_visits', y='referral_pct',
                          size='villages_covered',
                          color='health_worker_name',
                          title="Visits vs Referral Rate",
                          template="plotly_dark")
        fig3.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520")
        st.plotly_chart(fig3, use_container_width=True)

# ── TAB 3: VILLAGE HEALTH ──────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-header'>Village Health Summary</div>", unsafe_allow_html=True)
    village_df = pd.read_sql("""
        SELECT village,
            COUNT(*) as total_patients,
            COUNT(DISTINCT diagnosis) as diseases,
            COUNT(DISTINCT health_worker_id) as workers,
            ROUND(AVG(age),1) as avg_age,
            ROUND(AVG(temperature_c),1) as avg_temp,
            SUM(CASE WHEN temperature_c>38.5 THEN 1 ELSE 0 END) as fever_cases,
            SUM(is_child_under_5) as children_under_5,
            SUM(is_elderly) as elderly,
            SUM(referred_to_hospital) as referrals,
            ROUND(100.0*SUM(referred_to_hospital)/COUNT(*),1) as referral_pct
        FROM raw_patients GROUP BY village ORDER BY total_patients DESC
    """, engine)

    col1, col2 = st.columns(2)
    with col1:
        fig4 = px.bar(village_df, x='village', y='total_patients',
                      color='fever_cases',
                      title="Patients per Village",
                      template="plotly_dark",
                      color_continuous_scale='OrRd')
        fig4.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520", xaxis_tickangle=-30)
        st.plotly_chart(fig4, use_container_width=True)
    with col2:
        fig5 = px.scatter(village_df,
                          x='total_patients', y='referral_pct',
                          size='fever_cases', color='village',
                          title="Village Size vs Referral Rate",
                          template="plotly_dark")
        fig5.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520")
        st.plotly_chart(fig5, use_container_width=True)

    st.dataframe(village_df, use_container_width=True, hide_index=True)

# ── TAB 4: DISEASE TRENDS ──────────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-header'>Disease Trends Over Time</div>", unsafe_allow_html=True)
    trend_df = pd.read_sql("""
        SELECT diagnosis, visit_month,
            COUNT(*) as cases,
            SUM(referred_to_hospital) as referrals
        FROM raw_patients
        GROUP BY diagnosis, visit_month
        ORDER BY visit_month, cases DESC
    """, engine)

    fig6 = px.line(trend_df, x='visit_month', y='cases',
                   color='diagnosis',
                   title="Monthly Disease Cases Over Time",
                   template="plotly_dark",
                   markers=True,
                   color_discrete_sequence=px.colors.qualitative.Set2)
    fig6.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520")
    st.plotly_chart(fig6, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        total_disease = pd.read_sql("""
            SELECT diagnosis, COUNT(*) as total
            FROM raw_patients GROUP BY diagnosis ORDER BY total DESC
        """, engine)
        fig7 = px.pie(total_disease, values='total', names='diagnosis',
                      title="Overall Disease Distribution",
                      template="plotly_dark",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig7.update_layout(paper_bgcolor="#0d1520")
        st.plotly_chart(fig7, use_container_width=True)
    with col2:
        fig8 = px.bar(trend_df, x='diagnosis', y='cases',
                      color='visit_month',
                      title="Cases by Disease and Month",
                      template="plotly_dark",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig8.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520", xaxis_tickangle=-30)
        st.plotly_chart(fig8, use_container_width=True)

# ── TAB 5: VULNERABLE GROUPS ───────────────────────────────────────────────
with tab5:
    st.markdown("<div class='section-header'>Vulnerable Population Tracker</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    children = pd.read_sql("""
        SELECT village, COUNT(*) as cases, diagnosis
        FROM raw_patients WHERE is_child_under_5=1
        GROUP BY village, diagnosis ORDER BY cases DESC LIMIT 10
    """, engine)

    elderly = pd.read_sql("""
        SELECT village, COUNT(*) as cases, diagnosis
        FROM raw_patients WHERE is_elderly=1
        GROUP BY village, diagnosis ORDER BY cases DESC LIMIT 10
    """, engine)

    high_risk = pd.read_sql("""
        SELECT village, COUNT(*) as cases, diagnosis
        FROM raw_patients WHERE is_high_risk_disease=1
        GROUP BY village, diagnosis ORDER BY cases DESC LIMIT 10
    """, engine)

    with col1:
        st.markdown("#### 👶 Children Under 5")
        if len(children) > 0:
            fig9 = px.bar(children, x='cases', y='village',
                          color='diagnosis', orientation='h',
                          template="plotly_dark",
                          color_discrete_sequence=px.colors.qualitative.Pastel)
            fig9.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520", height=350)
            st.plotly_chart(fig9, use_container_width=True)
        else:
            st.info("No data yet")

    with col2:
        st.markdown("#### 👴 Elderly Patients (60+)")
        if len(elderly) > 0:
            fig10 = px.bar(elderly, x='cases', y='village',
                           color='diagnosis', orientation='h',
                           template="plotly_dark",
                           color_discrete_sequence=px.colors.qualitative.Set3)
            fig10.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520", height=350)
            st.plotly_chart(fig10, use_container_width=True)
        else:
            st.info("No data yet")

    with col3:
        st.markdown("#### 🦠 High Risk Disease Cases")
        if len(high_risk) > 0:
            fig11 = px.bar(high_risk, x='cases', y='village',
                           color='diagnosis', orientation='h',
                           template="plotly_dark",
                           color_discrete_sequence=px.colors.qualitative.Set2)
            fig11.update_layout(paper_bgcolor="#0d1520", plot_bgcolor="#0d1520", height=350)
            st.plotly_chart(fig11, use_container_width=True)
        else:
            st.info("No data yet")

    age_df = pd.read_sql("""
        SELECT
            CASE
                WHEN age < 5  THEN 'Under 5'
                WHEN age < 18 THEN 'Child 5-17'
                WHEN age < 60 THEN 'Adult 18-59'
                ELSE 'Senior 60+'
            END as age_group,
            diagnosis, COUNT(*) as cases
        FROM raw_patients
        GROUP BY age_group, diagnosis
        ORDER BY cases DESC
    """, engine)

    if len(age_df) > 0:
        fig12 = px.sunburst(age_df, path=['age_group', 'diagnosis'],
                            values='cases',
                            title="Disease Distribution by Age Group",
                            template="plotly_dark",
                            color_discrete_sequence=px.colors.qualitative.Set2)
        fig12.update_layout(paper_bgcolor="#0d1520")
        st.plotly_chart(fig12, use_container_width=True)
    else:
        st.info("No data yet")