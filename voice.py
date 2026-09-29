from flask import Flask, request, send_file
import edge_tts
import asyncio

app = Flask(__name__)

@app.route("/tts")
def tts():

    text = request.args.get("text", "Hello")

    async def generate():
        await edge_tts.Communicate(
            text,
            "en-US-AnaNeural"
        ).save("speech.mp3")

    asyncio.run(generate())

    return send_file(
        "speech.mp3",
        mimetype="audio/mpeg"
    )
