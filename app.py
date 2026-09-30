import os
import asyncio
from flask import Flask, request, send_file
import edge_tts
from pydub import AudioSegment

app = Flask(__name__)

@app.route("/tts")
def tts():
    text = request.args.get("text", "Hello")

    async def generate():
        communicate = edge_tts.Communicate(text, "en-US-AnaNeural", rate="+15%", pitch="+10Hz")
        await communicate.save("speech.mp3")
        
        # Convert MP3 to clean 16kHz Mono WAV for the ESP32
        sound = AudioSegment.from_mp3("speech.mp3")
        sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        sound.export("speech.wav", format="wav")

    asyncio.run(generate())
    return send_file("speech.wav", mimetype="audio/wav")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
