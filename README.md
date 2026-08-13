# 📚 AutoAttend - Automated Student Attendance Tracker

AutoAttend is an AI-powered, cloud-native web application designed to help students track and monitor their class attendance effortlessly. Built with Python, Streamlit, and Supabase, it automatically processes university schedules, logs daily attendance, visualizes subject-wise percentages, and generates multi-sheet Excel reports.

---

## 🌟 Key Features

* **AI Timetable Parsing:** Uses Vision LLMs (Hugging Face Inference API / NVIDIA NIM) to extract subjects, days, and times from raw timetable images/PDFs.
* **Daily Attendance Logger:** Quick form to log class status (*Attended*, *Missed*, or *Cancelled*).
* **Live Dashboard:** Displays real-time metrics, overall attendance percentage, and subject-wise progress bars.
* **Multi-Sheet Excel Export:** Dynamically generates a downloadable `.xlsx` workbook containing a summary sheet and separate tabs for each individual subject.
* **Cloud Storage & Fast Sync:** Powered by Supabase PostgreSQL for zero-latency data persistence.
* **100% Free & Open Source:** Hosted on Hugging Face Spaces with zero infrastructure costs.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Database:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Data Processing & Excel:** `pandas` & `openpyxl`
* **AI Vision Inference:** `huggingface_hub` (InferenceClient)
* **Hosting Platform:** [Hugging Face Spaces](https://huggingface.co/spaces)

---

## 📁 Project Structure

```text
attendance-tracker/
├── .streamlit/
│   └── secrets.toml          # Local API credentials (Git-ignored)
├── app.py                    # Main Streamlit application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
