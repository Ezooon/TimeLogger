from aitool import client


def send(entries, prompt, previous_messages=[], on_successes=lambda x: None, on_failure=lambda x: None):
    entries_text = "\n\n".join(map(str, entries))
    previous_messages_text = "\n\n".join(map(str, previous_messages))
    try:
        complation = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You're Time Logger an application that let's the user write entries about their day."
                               "You're purpose is to help the user navigate and document their life."
                               "Don't use Markdown"  # "You respond in Kivy markup."
                },
                # {  # ToDo this is making the chatbot thinks it can interface with all of the features,
                #        #  which is good idea for later
                #     "role": "system",
                #     "content": """Time Logger Features:
                #                     Working Features:
                #                     1. Write new entries in few seconds.
                #                     2. Tag entries.
                #                     3. Search and filter entries with date and tags.
                #                     4. Attach files to entries.
                #                     5. Generate social media posts from your loaded entries.
                #                     6. Post on X.
                #                     7. Chat about your day(s) with a chatbot with access to your loaded entries.
                #
                #                     Under Development:
                #                     1. Continuous Logging.
                #                     2. Post on Facebook.
                #                     3. Post on LinkedIn.
                #                     """
                # },
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
