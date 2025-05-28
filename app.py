import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Transkrypcja audio po polsku", layout="centered")
st.title("📝 Transkrypcja audio (PL) z Whisper")

uploaded_file = st.file_uploader("Wgraj plik audio (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    with st.spinner("Transkrypcja w toku... może to potrwać chwilę."):
        # Zapisz plik tymczasowo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Załaduj model
        model = whisper.load_model("base")
        
        # Transkrypcja
        result = model.transcribe(tmp_path, language="pl")
        transcription = result["text"]

        # Usuń plik tymczasowy
        os.remove(tmp_path)

        st.success("✅ Transkrypcja zakończona!")
        st.subheader("📄 Tekst:")
        st.write(transcription)

        st.download_button("📥 Pobierz transkrypcję jako plik .txt", transcription, file_name="transkrypcja.txt")
