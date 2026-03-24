from openai import OpenAI
import subprocess
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()



client = OpenAI(
    api_key="GJksvW162RY0py9Mt3b3pzXdQbHXpiPh",
    base_url=""
)

completion = client.chat.completions.create(
    model= "qwen3-coder:30b", #"qwen2.5-coder:7b",#"qwen3-coder:30b" "gemma3:27b", 
    messages=[
        {
            "role": "user",
            "content": "Write a sentence telling a person they skipped an important step of the coffee preparation procedure. "
        }
    ],
)

response= completion.choices[0].message.content

print(response)


with client.audio.speech.with_streaming_response.create(
    model="kokoro:82m",
    input= response,
    voice="af_sky" # more voices: af_sky, am_adam, more voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
) as response:
    response.stream_to_file("audio.wav")

# Use subprocess to play the audio with aplay
#subprocess.run(["aplay", "audio.wav"])

# Load your sound file
sound = pygame.mixer.Sound("audio.wav")

# Play the soun
print(os.path.exists("audio.wav"))
sound.play()

pygame.time.wait(int(sound.get_length() * 1000))
