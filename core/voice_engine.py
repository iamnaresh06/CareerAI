from gtts import gTTS
import os


def generate_voice(feedback_text, media_path, username):
    filename = f"feedback_{username}.mp3"
    file_path = os.path.join(media_path, filename)

    tts = gTTS(text=feedback_text, lang='en')
    tts.save(file_path)

    return filename