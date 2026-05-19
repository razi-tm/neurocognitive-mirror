from __future__ import annotations

from datetime import date
import json
import pandas as pd
import plotly.express as px
import streamlit as st

from analytics import correlation_table, outliers, prepare_frame, rolling_summary
from cognitive_tests import digit_span_component, reaction_time_component, stroop_component
from demo_data import generate_demo_data
from narrative import generate_narrative
from utils import download_link, html_report, load_records, pdf_report_bytes, save_records

st.set_page_config(page_title="Neurocognitive Mirror", page_icon="🧠", layout="wide")
st.title("Neurocognitive Mirror MVP")
st.caption("Privacy-first cognitive self-tracking with local JSON persistence.")

if "records" not in st.session_state:
    st.session_state.records = load_records()

with st.sidebar:
    st.header("Data")
    if st.button("Load deterministic demo data"):
        st.session_state.records = generate_demo_data().to_dict("records")
        save_records(st.session_state.records)
        st.success("Demo data loaded")
    if st.button("Clear local data"):
        st.session_state.records = []
        save_records([])
    st.write(f"Records: {len(st.session_state.records)}")

tab_dash, tab_tests, tab_entry, tab_report = st.tabs(["Dashboard", "Cognitive tests", "Self report", "Narrative & export"])

df = prepare_frame(pd.DataFrame(st.session_state.records)) if st.session_state.records else pd.DataFrame()

with tab_dash:
    if df.empty:
        st.info("Load demo data or add a session.")
    else:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("CEI", f"{df['cei'].iloc[-1]:.1f}", f"{rolling_summary(df).get('cei_delta',0):+.1f}")
        k2.metric("Digit span", int(df['digit_span'].iloc[-1]))
        k3.metric("Reaction time", f"{df['reaction_time_ms'].iloc[-1]:.0f} ms")
        k4.metric("Stroop accuracy", f"{df['stroop_accuracy'].iloc[-1]:.0%}")
        st.plotly_chart(px.line(df, x="date", y=["cei", "digit_span_ma4", "stroop_accuracy_ma4"], title="Longitudinal trends and moving averages"), use_container_width=True)
        st.plotly_chart(px.scatter(df, x="sleep_quality", y="digit_span", color="stress", trendline="ols", title="Sleep vs working memory"), use_container_width=True)
        st.plotly_chart(px.imshow(correlation_table(df), text_auto=True, title="Correlation heatmap"), use_container_width=True)
        st.subheader("Outliers")
        st.dataframe(outliers(df, "reaction_time_ms"), use_container_width=True)

with tab_tests:
    st.subheader('Cognitive tests')
    st.caption('Run each quick task, then paste JSON outputs into Self report.')
    st.info('Tip: complete tests in order for a smoother flow: Digit Span → Reaction Time → Stroop.')
    c1, c2 = st.columns([1, 1])
    with c1:
        digit_span_component()
        reaction_time_component()
    with c2:
        stroop_component()
    st.warning('Current MVP limitation: test components cannot write directly to Streamlit session state here, so copy/paste JSON manually.')

with tab_entry:
    st.subheader("Add session")
    with st.form("session"):
        c1, c2, c3 = st.columns(3)
        d = c1.date_input("Date", date.today())
        sleep = c1.slider("Sleep quality", 1.0, 10.0, 7.0, 0.1)
        stress = c2.slider("Stress", 1.0, 10.0, 4.0, 0.1)
        alertness = c3.slider("Alertness", 1.0, 10.0, 6.0, 0.1)
        digit = c1.number_input("Digit span", 1, 20, 7)
        rt = c2.number_input("Reaction time ms", 100.0, 1500.0, 280.0)
        stroop_acc = c3.number_input("Stroop accuracy", 0.0, 1.0, 0.85)
        stroop_int = c3.number_input("Stroop interference ms", -200.0, 800.0, 120.0)
        pasted = st.text_area("Optional copied test JSON")
        notes = st.text_area("Notes")
        if st.form_submit_button("Save session"):
            record = {"date": d.isoformat(), "sleep_quality": sleep, "stress": stress, "alertness": alertness, "digit_span": digit, "reaction_time_ms": rt, "stroop_accuracy": stroop_acc, "stroop_interference_ms": stroop_int, "notes": notes, "source": "manual"}
            if pasted.strip():
                try:
                    record.update({k: v for k, v in json.loads(pasted).items() if not k.endswith("events")})
                except json.JSONDecodeError:
                    st.error("Invalid JSON ignored")
            st.session_state.records.append(record)
            save_records(st.session_state.records)
            st.success("Saved")

with tab_report:
    if df.empty:
        st.info("No data yet.")
    else:
        narrative = generate_narrative(df)
        st.markdown(narrative)
        html = html_report(df, narrative)
        pdf = pdf_report_bytes(df, narrative)
        st.markdown(download_link(html, "neurocognitive_report.html", "text/html"), unsafe_allow_html=True)
        st.markdown(download_link(pdf, "neurocognitive_report.pdf", "application/pdf"), unsafe_allow_html=True)
