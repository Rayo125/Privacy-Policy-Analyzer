# import streamlit as st
# import re
# import PyPDF2

# # --- Alerts with regex patterns (flexible matching) ---
# ALERTS = {
#     r"\bshare(s|d)? with third[- ]?part(y|ies)\b": "⚠ Data Sharing",
#     r"\bsell(s|ing)? data\b": "⚠ Data Selling",
#     r"\b(location|geolocation)\b": "⚠ Location Tracking",
#     r"\bcookies?\b": "⚠ Cookie Usage",
#     r"\btrack(ing)?\b": "⚠ User Tracking",
#     r"\badvertis(e|ing|ement|ements)\b": "⚠ Ad Targeting"
#     # Add more if needed
# }


# # --- Risk level based on number of alerts ---
# def risk_level(count):
#     if count == 0:
#         return "Low"
#     elif count <= 2:
#         return "Medium"
#     else:
#         return "High"


# # --- PDF reader helper ---
# def read_pdf(file):
#     try:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#         return text
#     except Exception as e:
#         return f"Error reading PDF: {e}"


# # --- Scan function ---
# def scan_text(text):
#     found_alerts = []
#     for pattern, alert in ALERTS.items():
#         if re.search(pattern, text, re.IGNORECASE):
#             found_alerts.append(alert)
#     return found_alerts, risk_level(len(found_alerts))


# # --- Streamlit UI ---
# st.title("🔍 Privacy Policy & Terms Risk Scanner")

# uploaded_file = st.file_uploader("Upload a file (TXT or PDF)", type=['txt', 'pdf'])
# pasted_text = st.text_area("Or paste your Privacy Policy / Terms & Conditions here:", height=300)

# text = ""

# # Handle file upload
# if uploaded_file is not None:
#     if uploaded_file.type == "text/plain":
#         try:
#             text = uploaded_file.read().decode("utf-8", errors="ignore")
#         except Exception:
#             st.error("Could not read the TXT file. Please check encoding.")
#     elif uploaded_file.type == "application/pdf":
#         text = read_pdf(uploaded_file)

# # Handle pasted text if no file uploaded
# elif pasted_text.strip():
#     text = pasted_text

# # --- Show results ---
# if text:
#     alerts, risk = scan_text(text)
#     st.header("📑 Scan Report")

#     if alerts:
#         for alert in alerts:
#             st.warning(alert)
#     else:
#         st.info("✅ No alerts found.")

#     st.subheader(f"🔒 Overall Risk Level: **{risk}**")


# import streamlit as st
# import re
# import PyPDF2
# import requests
# from streamlit_lottie import st_lottie
# import plotly.graph_objects as go

# # --- Alerts with regex patterns (flexible matching) ---
# ALERTS = {
#     r"\bshare(s|d)? with third[- ]?part(y|ies)\b": "⚠ Data Sharing",
#     r"\bsell(s|ing)? data\b": "⚠ Data Selling",
#     r"\b(location|geolocation)\b": "⚠ Location Tracking",
#     r"\bcookies?\b": "⚠ Cookie Usage",
#     r"\btrack(ing)?\b": "⚠ User Tracking",
#     r"\badvertis(e|ing|ement|ements)\b": "⚠ Ad Targeting"
#     # Add more if needed
# }

# # --- Risk level based on number of alerts ---
# def risk_level(count):
#     if count == 0:
#         return "Low"
#     elif count <= 2:
#         return "Medium"
#     else:
#         return "High"

# # --- PDF reader helper ---
# def read_pdf(file):
#     try:
#         reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#         return text
#     except Exception as e:
#         return f"Error reading PDF: {e}"

# # --- Load Lottie animations ---
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_scan = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_t9gkkhz4.json")
# lottie_done = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_t9gkkhz4.json")

# # --- Scan function ---
# def scan_text(text):
#     found_alerts = []
#     for pattern, alert in ALERTS.items():
#         if re.search(pattern, text, re.IGNORECASE):
#             found_alerts.append(alert)
#     return found_alerts, risk_level(len(found_alerts))

# # --- Highlight risky keywords in text ---
# def highlight_alerts(text):
#     for pattern, alert in ALERTS.items():
#         text = re.sub(pattern, f"**:red[\\g<0> ({alert})]**", text, flags=re.IGNORECASE)
#     return text

# # --- Risk Gauge Meter ---
# def risk_gauge(risk):
#     level = {"Low": 20, "Medium": 50, "High": 90}[risk]
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=level,
#         gauge={'axis': {'range': [0, 100]},
#                'bar': {'color': "red" if risk=="High" else "orange" if risk=="Medium" else "green"}},
#         title={'text': f"Risk Level: {risk}"}
#     ))
#     st.plotly_chart(fig, use_container_width=True)

# # --- Streamlit UI ---
# st.title("🔍 Privacy Policy & Terms Risk Scanner")

# uploaded_file = st.file_uploader("Upload a file (TXT or PDF)", type=['txt', 'pdf'])
# pasted_text = st.text_area("Or paste your Privacy Policy / Terms & Conditions here:", height=300)

# text = ""

# # Handle file upload
# if uploaded_file is not None:
#     if uploaded_file.type == "text/plain":
#         try:
#             text = uploaded_file.read().decode("utf-8", errors="ignore")
#         except Exception:
#             st.error("Could not read the TXT file. Please check encoding.")
#     elif uploaded_file.type == "application/pdf":
#         text = read_pdf(uploaded_file)

# # Handle pasted text if no file uploaded
# elif pasted_text.strip():
#     text = pasted_text

# # --- Show results ---
# if text:
#     with st.spinner("🔍 Scanning your document..."):
#         alerts, risk = scan_text(text)

#     st_lottie(lottie_done, height=200, key="done")
#     st.header("📑 Scan Report")

#     if alerts:
#         for alert in alerts:
#             st.warning(alert)
#     else:
#         st.info("✅ No alerts found.")

#     st.subheader(f"🔒 Overall Risk Level: **{risk}**")
#     risk_gauge(risk)

#     st.markdown("### Highlighted Policy Text")
#     st.markdown(highlight_alerts(text), unsafe_allow_html=True)

#     st_lottie(lottie_scan, height=200, key="scan")


import streamlit as st
import re
import PyPDF2
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go

# --- Alerts with regex patterns and weights ---
ALERTS = {
    r"\bshare(s|d)? with third[- ]?part(y|ies)\b": ("⚠ Data Sharing", 30),
    r"\bsell(s|ing)? data\b": ("⚠ Data Selling", 50),
    r"\b(location|geolocation)\b": ("⚠ Location Tracking", 25),
    r"\bcookies?\b": ("⚠ Cookie Usage", 10),
    r"\btrack(ing)?\b": ("⚠ User Tracking", 20),
    r"\badvertis(e|ing|ement|ements)\b": ("⚠ Ad Targeting", 15)
}

MAX_SCORE = sum(weight for _, weight in ALERTS.values())

# --- Risk level scoring ---
def scan_text(text):
    found_alerts = []
    score = 0
    for pattern, (alert, weight) in ALERTS.items():
        if re.search(pattern, text, re.IGNORECASE):
            found_alerts.append(alert)
            score += weight

    # Normalize into percentage
    risk_percentage = int((score / MAX_SCORE) * 100)

    # Risk label
    if risk_percentage == 0:
        risk_label = "Low"
    elif risk_percentage <= 40:
        risk_label = "Medium"
    else:
        risk_label = "High"

    return found_alerts, risk_label, risk_percentage

# --- PDF reader helper ---
def read_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- Lottie animations loader ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_scan = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_t9gkkhz4.json")
lottie_done = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_t9gkkhz4.json")

# --- Highlight risky keywords in text ---
def highlight_alerts(text):
    for pattern, (alert, _) in ALERTS.items():
        text = re.sub(pattern, f"**:red[\\g<0> ({alert})]**", text, flags=re.IGNORECASE)
    return text

# --- Risk Gauge Meter ---
def risk_gauge(risk_label, risk_percentage):
    level = risk_percentage
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=level,
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "red" if risk_label == "High" else "orange" if risk_label == "Medium" else "green"}},
        title={'text': f"Risk Level: {risk_label}"}
    ))
    st.plotly_chart(fig, use_container_width=True)

# --- Streamlit UI ---
st.title("🔍 Privacy Policy & Terms Risk Scanner")

uploaded_file = st.file_uploader("Upload a file (TXT or PDF)", type=['txt', 'pdf'])
pasted_text = st.text_area("Or paste your Privacy Policy / Terms & Conditions here:", height=300)

text = ""

# Handle file upload
if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        try:
            text = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            st.error("Could not read the TXT file. Please check encoding.")
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)

# Handle pasted text if no file uploaded
elif pasted_text.strip():
    text = pasted_text

# --- Show results ---
if text:
    with st.spinner("🔍 Scanning your document..."):
        alerts, risk_label, risk_percentage = scan_text(text)

    st_lottie(lottie_done, height=200, key="done")
    st.header("📑 Scan Report")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.info("✅ No alerts found.")

    st.subheader(f"🔒 Overall Risk Level: **{risk_label} ({risk_percentage}%)**")
    risk_gauge(risk_label, risk_percentage)

    # Pie chart for distribution of issues
    if alerts:
        fig = go.Figure(data=[go.Pie(labels=alerts, values=[1]*len(alerts), hole=0.3)])
        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Highlighted Policy Text")
    st.markdown(highlight_alerts(text), unsafe_allow_html=True)

    st_lottie(lottie_scan, height=200, key="scan")

else:
    st.warning("Please upload a file or paste your Privacy Policy / Terms & Conditions.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

