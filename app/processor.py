import os
import whisper
import yt_dlp
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def transcribe_and_translate(file_path):
    """Detects Arabic, transcribes it, and translates with scholarly context."""
    # Load model (use 'base' for speed, 'medium' or 'large' for better Fusha/Dialect accuracy)
    model = whisper.load_model("base")
    
    # --- 1. LANGUAGE GUARDRAIL ---
    # We check the first 30 seconds to ensure it's Arabic
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    detected_lang = max(probs, key=probs.get)

    if detected_lang != "ar":
        return f"Error: Language detected as {detected_lang}.", "This app is restricted to Arabic content only."

    # --- 2. TRANSCRIPTION ---
    # Task is just transcribe to get the raw Arabic text (Fusha or Dialect)
    result = model.transcribe(file_path, language="ar")
    raw_arabic = result['text']
    
    # --- 3. CONTEXTUAL TRANSLATION (The 'Brain') ---
    llm = genai.GenerativeModel('gemini-2.5-flash')
    
    # We tell Gemini to act as a Scholar to handle texts like Al-Ajurrumiyyah
    prompt = f"""
    You are a professional translator and an expert in Classical Arabic (Fusha), 
    Arabic Grammar (Nahw), and Islamic Jurisprudence.
    
    Task: Translate this Arabic transcript into fluent, academic English. 
    Context: This may be a lecture by a scholar (like Ibn Uthaymin).
    Requirements:
    1. If you encounter grammatical terms (e.g., 'mubtada', 'khabar', 'mansub'), provide the English linguistic equivalent.
    2. Maintain the dignity of the scholarly tone.
    3. If there are dialectal gaps, use the context of the sentence to provide the best translation.
    
    Transcript: {raw_arabic}
    """
    
    response = llm.generate_content(prompt)
    return raw_arabic, response.text

def download_youtube(url):
    """Downloads YouTube audio to a high-quality temporary MP3."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_yt_audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "temp_yt_audio.mp3"