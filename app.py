import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import os
import subprocess

st.set_page_config(page_title="Transkrypcja audio (PL)", layout="centered")
st.title("🎙️ Transkrypcja audio z języka polskiego")

uploaded_file = st.file_uploader("Wgraj plik audio (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        audio_path = tmp_wav.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_in:
            tmp_in.write(uploaded_file.read())
            tmp_in.flush()
            subprocess.call([
                "ffmpeg", "-y", "-i", tmp_in.name,
                "-ar", "16000", "-ac", "1", audio_path
            ])

    with st.spinner("Transkrypcja w toku..."):
        model = WhisperModel("base", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language="pl")
        transcription = " ".join([segment.text for segment in segments])

        st.success("✅ Gotowe!")
        st.subheader("📄 Transkrypcja:")
        st.write(transcription)

        st.download_button("📥 Pobierz jako .txt", transcription, file_name="transkrypcja.txt")

    os.remove(audio_path)
    os.remove(tmp_in.name)
