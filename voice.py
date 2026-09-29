from flask import Flask, request, send_file
import edge_tts
import asyncio

app = Flask(__name__)

@app.route("/tts")
def tts():

    text = request.args.get("text", "Hello")

    async def generate():
        communicate = edge_tts.Communicate(
            text,
            "en-US-AnaNeural",
            rate="+15%",
            pitch="+10Hz"
        )
        await communicate.save("speech.mp3")

    asyncio.run(generate())

    return send_file(
        "speech.mp3",
        mimetype="audio/mpeg"
    )

app.run(host="0.0.0.0", port=5000)