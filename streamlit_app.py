# streamlit_app.py

import streamlit as st
import pandas as pd
import io
from api.processor import (
    validate_dataframe,
    compute_sum,
    generate_plot,
    parse_remote_file,
    parse_text_input
)

st.set_page_config(page_title="📊 Data Processor", layout="centered")
st.title("📊 Data Processor Interface")
st.write("Upload a CSV or JSON file, fetch one from a URL, or paste raw text.")

# Tabs for input modes
tab1, tab2, tab3 = st.tabs(["📁 Upload File", "🌐 Fetch from URL", "📝 Manual Text Entry"])

# 📁 Upload File Tab
with tab1:
    uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
            else:
                st.warning("Unsupported file format. Use CSV or JSON.")
                df = None
        except Exception as e:
            st.error(f"Failed to read file: {e}")
            df = None

        if df is not None:
            try:
                x, y = validate_dataframe(df)
                st.subheader("📄 Data Preview")
                st.dataframe(df)
                st.write(f"✅ Columns: {list(df.columns)}")
                st.write(f"📊 Rows: {len(df)}")

                if st.button("Process Uploaded File"):
                    with st.spinner("Processing..."):
                        total = compute_sum(y)
                        plot_uri = f"data:image/png;base64,{generate_plot(x, y)}"
                        st.success(f"✅ Sum: {total}")
                        st.image(plot_uri, caption="Scatter Plot", use_container_width=True)
            except Exception as e:
                st.error(str(e))

# 🌐 Fetch from URL Tab
with tab2:
    url_input = st.text_input("Enter URL to a CSV or JSON file")
    if url_input:
        try:
            x, y = parse_remote_file(url_input)
            df = pd.DataFrame({"x": x, "y": y})
            st.subheader("📄 Data Preview")
            st.dataframe(df)
            st.write(f"✅ Columns: {list(df.columns)}")
            st.write(f"📊 Rows: {len(df)}")

            if st.button("Process Remote File"):
                with st.spinner("Processing..."):
                    total = compute_sum(y)
                    plot_uri = f"data:image/png;base64,{generate_plot(x, y)}"
                    st.success(f"✅ Sum: {total}")
                    st.image(plot_uri, caption="Scatter Plot", use_container_width=True)
        except Exception as e:
            st.error(str(e))

# 📝 Manual Text Entry Tab
with tab3:
    sample = "x,y\n1,4\n2,5\n3,6"
    text_input = st.text_area("Paste CSV-style data", value=sample, height=150)
    if text_input:
        try:
            x, y = parse_text_input(text_input)
            df = pd.DataFrame({"x": x, "y": y})
            st.subheader("📄 Data Preview")
            st.dataframe(df)
            st.write(f"✅ Columns: {list(df.columns)}")
            st.write(f"📊 Rows: {len(df)}")

            if st.button("Process Text Input"):
                with st.spinner("Processing..."):
                    total = compute_sum(y)
                    plot_uri = f"data:image/png;base64,{generate_plot(x, y)}"
                    st.success(f"✅ Sum: {total}")
                    st.image(plot_uri, caption="Scatter Plot", use_container_width=True)
        except Exception as e:
            st.error(str(e))
