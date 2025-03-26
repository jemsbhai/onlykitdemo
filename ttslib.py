import os
import subprocess
from cartesia import Cartesia

# if os.environ.get("CARTESIA_API_KEY") is None:
#     raise ValueError("CARTESIA_API_KEY is not set")

##insecure
CARTESIA_API_KEY = "KEYHERE"

client = Cartesia(api_key=CARTESIA_API_KEY)


def speakout(text):

    data = client.tts.bytes(
        model_id="sonic-2",
        transcript=text,
        voice_id="IDHERE",  # dispatch voice
        # You can find the supported `output_format`s at https://docs.cartesia.ai/api-reference/tts/bytes
        output_format={
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
    )

    with open("output.wav", "wb") as f:
        f.write(data)
    
    # Play the file
    subprocess.run(["ffplay", "-autoexit", "-nodisp", "output.wav"])
    
    return "output.wav"

# # Play the file
# subprocess.run(["ffplay", "-autoexit", "-nodisp", "sonic-2.wav"])
