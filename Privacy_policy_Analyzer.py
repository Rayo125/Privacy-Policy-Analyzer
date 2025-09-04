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
MAX_FILE_SIZE_MB = 5  # Limit file uploads to 5MB

# --- Risk level scoring ---
def scan_text(text):
    found_alerts = []
    alert_counts = {}
    score = 0
    for pattern, (alert, weight) in ALERTS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_alerts.append(alert)
            alert_counts[alert] = len(matches)
            score += weight
    risk_percentage = int((score / MAX_SCORE) * 100)
    if risk_percentage == 0:
        risk_label = "Low"
    elif risk_percentage <= 40:
        risk_label = "Medium"
    else:
        risk_label = "High"
    return found_alerts, alert_counts, risk_label, risk_percentage

# --- PDF reader helper ---
def read_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text:
            raise ValueError("No extractable text found in PDF.")
        return text
    except Exception as e:
        return None, f"Error reading PDF: {e}"

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
    # Order patterns by length to avoid nested highlights
    sorted_alerts = sorted(ALERTS.items(), key=lambda x: -len(x[0]))
    for pattern, (alert, _) in sorted_alerts:
        text = re.sub(
            pattern,
            lambda m: f"**:red[{m.group(0)} ({alert})]**",
            text,
            flags=re.IGNORECASE,
        )
    return text

# --- Risk Gauge Meter ---
def risk_gauge(risk_label, risk_percentage):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "red" if risk_label == "High" else "orange" if risk_label == "Medium" else "green"}},
        title={'text': f"Risk Level: {risk_label}"}
    ))
    st.plotly_chart(fig, use_container_width=True)

# --- Streamlit UI ---
st.title("🔍 Privacy Policy & Terms Risk Scanner")

uploaded_file = st.file_uploader("Upload a file (TXT or PDF, max 5MB)", type=['txt', 'pdf'])
pasted_text = st.text_area("Or paste your Privacy Policy / Terms & Conditions here:", height=300)
text = ""

# --- File upload handling ---
if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"File too large! Max size: {MAX_FILE_SIZE_MB}MB.")
    else:
        filetype = uploaded_file.type
        # Robust type check
        if filetype in ["text/plain", "application/octet-stream"]:
            try:
                text = uploaded_file.read().decode("utf-8", errors="ignore")
            except Exception:
                st.error("Could not read the TXT file. Please check encoding.")
        elif filetype in ["application/pdf", "application/x-pdf"]:
            pdf_text, pdf_error = read_pdf(uploaded_file)
            if pdf_text is None:
                st.error(pdf_error)
            else:
                text = pdf_text
        else:
            st.error("Unsupported file type. Please upload TXT or PDF.")

# --- Pasted text handling (only if no file uploaded) ---
elif pasted_text.strip():
    text = pasted_text

# --- Show results ---
if text:
    with st.spinner("🔍 Scanning your document..."):
        alerts, alert_counts, risk_label, risk_percentage = scan_text(text)
    st_lottie(lottie_done, height=200, key="done")
    st.header("📑 Scan Report")
    if alerts:
        for alert in alerts:
            st.warning(f"Detected: {alert} ({alert_counts[alert]} occurrence{'s' if alert_counts[alert]>1 else ''})")
    else:
        st.info("✅ No alerts found.")

    st.subheader(f"🔒 Overall Risk Level: **{risk_label} ({risk_percentage}%)**")
    risk_gauge(risk_label, risk_percentage)

    # Pie chart for distribution of issues
    if alerts:
        fig = go.Figure(data=[go.Pie(labels=list(alert_counts.keys()), values=list(alert_counts.values()), hole=0.3)])
        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Highlighted Policy Text")
    highlighted = highlight_alerts(text)
    # Limit preview for very large texts
    preview = highlighted if len(highlighted) < 20000 else highlighted[:20000] + "\n... (truncated)"
    st.markdown(preview, unsafe_allow_html=True)
    st_lottie(lottie_scan, height=200, key="scan")

else:
    st.warning("Please upload a file or paste your Privacy Policy / Terms & Conditions.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
