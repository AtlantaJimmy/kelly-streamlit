from groq import Groq

client = Groq(api_key="gsk_EonNtb...")  # <-- paste your full key here

try:
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": "Write a one-line skeptical poem about AI."}]
    )
    print(resp.choices[0].message.content)
except Exception as e:
    print("Error:", e)
