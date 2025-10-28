import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Flow con Anuel 🔊", page_icon="🎤", layout="centered")

# --- TÍTULO Y PORTADA ---
st.title("🔥 Generador de Audio - Flow Anuel 🔥")

image = Image.open('anuel_portada.png')  # Reemplaza con una imagen de Anuel
st.image(image, width=400)

with st.sidebar:
    st.subheader("💬 Convierte tus frases con el flow de Anuel")
    st.write("Escribe un texto, selecciona el idioma y escucha cómo suena con actitud 💯")

# --- CREAR CARPETA TEMPORAL ---
os.makedirs("temp", exist_ok=True)

# --- FRASE DE INTRODUCCIÓN ---
st.subheader("🎶 Frase inspiradora de Anuel:")
st.write("“Alguna vez lo tuve todo, pero no era feliz... ahora tengo paz, y eso vale más que todo.” — *Anuel AA*")

st.markdown("¿Quieres escuchar tu texto con estilo? Escribe lo que quieras aquí abajo 👇")

# --- INPUT DE TEXTO ---
text = st.text_area("🎤 Escribe tu texto:", placeholder="Ejemplo: Real hasta la muerte, baby...")

# --- SELECCIÓN DE IDIOMA ---
option_lang = st.selectbox("🌍 Selecciona el idioma", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# --- FUNCIÓN DE CONVERSIÓN ---
def text_to_speech(text, lang):
    tts = gTTS(text, lang=lang)
    file_name = text[:15].replace(" ", "_") if text else "audio"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_path

# --- BOTÓN DE CONVERSIÓN ---
if st.button("🎧 Convertir a Audio"):
    if text.strip():
        audio_path = text_to_speech(text, lg)
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()

        st.success("🔥 ¡Tu audio está listo! Escúchalo con flow:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # --- DESCARGA ---
        with open(audio_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(audio_path)}">⬇️ Descargar Audio</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("😅 Escribe algo para convertirlo a audio, bro.")

# --- LIMPIEZA AUTOMÁTICA ---
def remove_old_files(days):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    limit = now - (days * 86400)
    for f in mp3_files:
        if os.path.getmtime(f) < limit:
            os.remove(f)

remove_old_files(7)

# --- FOOTER ---
st.markdown("---")
st.caption("💿 App creada con el flow de Anuel AA | Real Hasta La Muerte 💀")
