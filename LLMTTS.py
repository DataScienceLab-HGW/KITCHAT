from openai import OpenAI
import pygame
import os


class LLMTTS:

    def __init__(self, api_key, base_url):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Create client
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def generate_text(self, prompt):
        completion = self.client.chat.completions.create(
            model="qwen3-coder:30b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        response = completion.choices[0].message.content
        print(response)
        return response

    def text_to_speech(self, text, filename="audio.wav"):
        with self.client.audio.speech.with_streaming_response.create(
            model="kokoro:82m",
            input=text,
            voice="af_sky"
        ) as response:
            response.stream_to_file(filename)

        return filename

    def play_audio(self, filename):
        print(os.path.exists(filename))
        # we want to make sure that no other sounds are being played
        pygame.mixer.stop()

        sound = pygame.mixer.Sound(filename)
        sound.play()

        pygame.time.wait(int(sound.get_length() * 1000))

    def speak(self, prompt):
        text = self.generate_text(prompt)
        audio_file = self.text_to_speech(text)
        self.play_audio(audio_file)


