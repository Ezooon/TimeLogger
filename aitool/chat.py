import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def send(entries, prompt, previous_messages=[]):
    entries_text = "\n\n".join(map(str, entries))
    previous_messages_text = "\n\n".join(map(str, previous_messages))

    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You give the user helpful responses using entries from their history"
            },
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "assistant",
                "content": f"These are the entries: \n{entries_text}",
            },
            {
                "role": "assistant",
                "content": f"Here is the chat history: \n{previous_messages_text}",
            },
        ],
        model="llama3-8b-8192",
        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        stream=True
    )

print(send())
