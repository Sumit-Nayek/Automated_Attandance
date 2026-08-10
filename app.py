import streamlit as st
import pandas as pd
from datetime import date
import io
from supabase import create_client, Client

# --- 1. SUPABASE DATABASE CONNECTION ---
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Page Title & Layout
st.set_page_config(page_title="AutoAttend", page_icon="📚", layout="wide")
st.title("📚 AutoAttend Student Dashboard")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📝 Log Attendance", "📊 Dashboard Stats", "📥 Export Excel"])

# --- TAB 1: DAILY LOGGING ---
with tab1:
    st.subheader("Mark Today's Attendance")
    
    with st.form("attendance_form", clear_on_submit=True):
        selected_date = st.date_input("Date", date.today())
        # In full version, subjects populate from parsed timetable
        subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "Computer Science", "Chemistry"])
        status = st.radio("Status", ["Attended", "Missed", "Cancelled"], horizontal=True)
        
        submit = st.form_submit_button("Submit Entry")
        
        if submit:
            # Insert record directly into Supabase
            data = {
                "log_date": str(selected_date),
                "subject": subject,
                "status": status
            }
            response = supabase.table("attendance_logs").insert(data).execute()
            st.success(f"Logged {subject} as '{status}' for {selected_date}!")

# --- TAB 2: DASHBOARD STATS ---
with tab2:
    st.subheader("Attendance Overview")
    
    # Fetch all records from Supabase
    response = supabase.table("attendance_logs").select("*").execute()
    logs = response.data
    
    if logs:
        df = pd.DataFrame(logs)
        
        # Calculate high-level metrics
        total_classes = len(df[df['status'] != 'Cancelled'])
        attended_classes = len(df[df['status'] == 'Attended'])
        
        overall_pct = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        
        # Metric Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Attendance", f"{overall_pct:.1f}%")
        col2.metric("Total Attended", attended_classes)
        col3.metric("Total Missed", len(df[df['status'] == 'Missed']))
        
        st.divider()
        st.write("### Subject Breakdown")
        
        # Subject-wise percentage calculation
        subjects = df['subject'].unique()
        for sub in subjects:
            sub_df = df[df['subject'] == sub]
            sub_total = len(sub_df[sub_df['status'] != 'Cancelled'])
            sub_attended = len(sub_df[sub_df['status'] == 'Attended'])
            sub_pct = (sub_attended / sub_total * 100) if sub_total > 0 else 0
            
            st.write(f"**{sub}**: {sub_pct:.1f}% ({sub_attended}/{sub_total} classes)")
            st.progress(int(sub_pct) / 100)
    else:
        st.info("No logs found. Start by marking your attendance in Tab 1!")

# --- TAB 3: EXCEL EXPORT ---
with tab3:
    st.subheader("Download Formatted Excel File")
    st.write("Generates an Excel workbook with a separate sheet for each subject.")
    
    if st.button("Generate Excel File"):
        response = supabase.table("attendance_logs").select("*").execute()
        logs = response.data
        
        if logs:
            df = pd.DataFrame(logs)
            
            # Write multi-sheet Excel into memory buffer
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                # Summary Sheet
                df.to_excel(writer, sheet_name='All_Logs', index=False)
                
                # Subject Specific Sheets
                for sub in df['subject'].unique():
                    sub_df = df[df['subject'] == sub]
                    # Format sheet name safely (max 31 chars)
                    sheet_title = sub[:30]
                    sub_df.to_excel(writer, sheet_name=sheet_title, index=False)
            
            # Download Button
            st.download_button(
                label="⬇️ Download .xlsx File",
                data=buffer.getvalue(),
                file_name=f"Attendance_Report_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No data to export.")
