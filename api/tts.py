from mutagen.mp3 import MP3
import tempfile

def synthesize_text(text: str) -> bytes:
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    audio_data = response.audio_content

    if not audio_data:
        print("❌ Google TTS returned empty audio content.")
    else:
        print(f"✅ Audio content generated: {len(audio_data)} bytes")

        # ✅ 임시 파일에 저장 후 길이 측정
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_data)
            tmp.flush()
            audio = MP3(tmp.name)
            print(f"📏 MP3 Duration: {audio.info.length:.2f} seconds")

    return audio_data
