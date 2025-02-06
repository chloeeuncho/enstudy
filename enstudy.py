import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import streamlit as st
import os

# 음성 녹음 함수
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 마이크를 켜고 말씀해 주세요!")
        audio = r.listen(source)
    return audio

# 음성을 텍스트로 변환 함수
def speech_to_text(audio):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio, language="ko-KR")
        return text
    except sr.UnknownValueError:
        return "음성을 인식할 수 없습니다."
    except sr.RequestError:
        return "음성 인식 서비스에 접근할 수 없습니다."

# 텍스트를 영어로 번역하는 함수
def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest="en")
    return translation.text

# TTS (Text-to-Speech) 생성 함수
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    output_file = "output.mp3"
    tts.save(output_file)
    return output_file

# Streamlit UI 구성
st.set_page_config(page_title="🎧 음성 인식 & 번역기", page_icon="🎤", layout="centered")
st.title("🎤 음성 인식 & 번역기")

# 페이지 설명 추가
st.markdown("""
### 👩‍🏫 영어 공부를 더 재미있게! 🎧
이 앱을 사용하여 여러분의 음성을 텍스트로 변환하고, 번역까지 해보세요! 
마지막으로, 번역된 텍스트를 음성으로 변환하여 들을 수 있어요. 
영어 공부를 재미있게 할 수 있는 기회! 🎶
""")

# 음성 녹음 버튼
if st.button("🎙️ 음성 녹음 시작", key="record_button", help="클릭 후 마이크로 음성을 입력하세요"):
    with st.spinner("음성을 인식 중... 잠시만 기다려 주세요!"):
        audio = record_audio()
        original_text = speech_to_text(audio)
        if "음성을 인식할 수 없습니다." in original_text or "음성 인식 서비스에 접근할 수 없습니다." in original_text:
            st.error(original_text)
        else:
            st.subheader("📜 원본 텍스트")
            st.write(f"**{original_text}**")

            # 번역
            translated_text = translate_to_english(original_text)
            st.subheader("🌍 번역된 텍스트 (영어)")
            st.write(f"**{translated_text}**")

            # TTS 음성 파일 생성
            output_file = text_to_speech(translated_text)
            st.subheader("🔊 번역된 음성 듣기")
            st.audio(output_file, format="audio/mp3")
            st.success("🎉 음성 변환이 완료되었습니다!")

# 앱 종료 시 생성된 mp3 파일 삭제
if os.path.exists("output.mp3"):
    os.remove("output.mp3")

# 추가적인 스타일링
st.markdown("""
<style>
    .stButton>button {
        background-color: #FFB6C1;
        color: #FFFFFF;
        font-size: 20px;
        border-radius: 10px;
        padding: 15px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FF69B4;
    }
    .stTitle {
        color: #FF1493;
        font-size: 36px;
    }
    .stText {
        font-size: 18px;
        color: #4B0082;
    }
    .stSubheader {
        color: #8A2BE2;
    }
</style>
""", unsafe_allow_html=True)
