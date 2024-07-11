import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


if __name__ == "__main__":
    chat_completion = client.chat.completions.create(
        messages=[
            # {
            #     "role": "system",
            #     "content": "you use the user entries to generate 3 Twitter posts."
            # },
            {
                "role": "user",
                "content": "Can I send you images?",
            }
        ],
        model="llama3-8b-8192",
        # response_format={"type": "json_object"},

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.75,
    )

    print(chat_completion.choices[0].message.content)
