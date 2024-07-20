from aitool import client


def send(entries, prompt, previous_messages=[], on_successes=lambda x: None, on_failure=lambda x: None):
    entries_text = "\n\n".join(map(str, entries))
    previous_messages_text = "\n\n".join(map(str, previous_messages))
    try:
        complation = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You give the user helpful responses using entries from their history"
                },
                {
                    "role": "assistant",
                    "content": f"User entries: \n{entries_text}",
                },
                {
                    "role": "assistant",
                    "content": f"chat history: \n{previous_messages_text}",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="llama3-70b-8192",
            temperature=0.4
            # Controls randomness: lowering results in less random completions.
            # As the temperature approaches zero, the model will become deterministic
            # and repetitive.

            # stream=True
        )
        on_successes(complation.choices[0].message.content)
    except Exception as e:
        on_failure(e)
