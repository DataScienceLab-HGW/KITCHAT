from openai import OpenAI

client = OpenAI(
    api_key="GJksvW162RY0py9Mt3b3pzXdQbHXpiPh",
    base_url=""
)

completion = client.chat.completions.create(
    model="qwen2.5-coder:7b",#"qwen3-coder:30b" "gemma3:27b", 
    messages=[
        {
            "role": "user",
            "content": "Write a sentence with 10 words"
        }
    ],
)

print(completion.choices[0].message.content)
