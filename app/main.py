import streamlit as st
import os
from processor import transcribe_and_translate, download_youtube

st.set_page_config(page_title="Lisaan AI", page_icon="🌙", layout="wide")

# Custom CSS for a clean look
st.markdown("""<style> .main { background-color: #f5f7f9; } </style>""", unsafe_allow_html=True)

st.title("🌙 Lisaan (لسان)")
st.markdown("##### Expert Arabic-to-English Translation for Scholars and Students")

tab1, tab2 = st.tabs(["📁 Local Video/Audio", "🔗 YouTube Link"])

# --- Tab 1: Manual Upload ---
with tab1:
    uploaded_file = st.file_uploader("Upload an Arabic recording", type=["mp4", "mov", "mp3", "m4a"])
    if uploaded_file:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Process Upload"):
            with st.spinner("Analyzing audio..."):
                ar, en = transcribe_and_translate(temp_path)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("Arabic Transcript")
                    st.write(ar)
                with col2:
                    st.success("English Translation")
                    st.write(en)
                os.remove(temp_path)

# --- Tab 2: YouTube ---
with tab2:
    yt_url = st.text_input("Enter YouTube URL (e.g., Ibn Uthaymin Lecture)")
    if yt_url:
        if st.button("Download & Translate"):
            with st.spinner("Fetching from YouTube and processing..."):
                audio_file = download_youtube(yt_url)
                ar, en = transcribe_and_translate(audio_file)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("Arabic Transcript")
                    st.write(ar)
                with col2:
                    st.success("English Translation")
                    st.write(en)
                
                if os.path.exists(audio_file):
                    os.remove(audio_file)